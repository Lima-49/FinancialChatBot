from typing import Optional, Any, List
from pathlib import Path
import tempfile
import re
from docling.document_converter import DocumentConverter
import pikepdf
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

class PDFService:
    """
    Serviço para converter PDFs (incluindo protegidos por senha) em DataFrames.
    Usa Docling (DocumentConverter) para gerar HTML e pandas para parsear tabelas.
    """

    def __init__(self, converter: Optional[DocumentConverter] = None) -> None:
        self.converter = converter or DocumentConverter()


    @staticmethod
    def _write_decrypted_tempfile(src: Path, password: str) -> Path:
        """
        Descriptografa `src` usando pikepdf e salva em um arquivo temporário.
        Retorna o Path para o arquivo criado.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp_path = Path(tmp.name)
        try:
            pdf = pikepdf.open(str(src), password=password)
            pdf.save(str(tmp_path))
            return tmp_path
        except Exception as e:
            # limpar arquivo temporário em caso de falha
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass

    def convert_with_optional_password(self, pdf_path: str | Path, password: Optional[str] = None):
        """
        Tenta converter com DocumentConverter. Se falhar por proteção e `password` estiver
        presente, descriptografa e reconverte usando um temp file.
        Retorna o objeto result do DocumentConverter (conforme API do docling).
        """
        pdf_path = Path(pdf_path)
        try:
            return self.converter.convert(str(pdf_path))
        except Exception as e:
            print(e)
            if not password:
                print("PDF protegido e sem senha fornecida.")
            # descriptografa para temp e tenta novamente
            temp_path = None
            try:
                temp_path = self._write_decrypted_tempfile(pdf_path, password)
                print("Tentando converter %s (decrypted)", temp_path)
                return self.converter.convert(str(temp_path))
            except Exception as e2:
                print("Falha ao converter após descriptografia: %s", e2)
            finally:
                if temp_path is not None:
                    try:
                        temp_path.unlink(missing_ok=True)
                    except Exception:
                        print("Não foi possível remover tempfile %s", temp_path)

    @staticmethod
    def _find_credit_amount(html_soup: BeautifulSoup, phrase: str) -> Optional[str]:
        paragraphs = html_soup.find_all("p")
        for p in paragraphs:
            if phrase.lower() in p.text.lower():
                # procurar próximo parágrafo com valor
                next_sibling = p.find_next_sibling("p")
                if "R$" in p.text:
                    return p.text.strip()
                while next_sibling:
                    if "R$" in next_sibling.text:
                        return next_sibling.text.strip()
                    next_sibling = next_sibling.find_next_sibling("p")
        return None

    @staticmethod
    def _find_value_index_in_df(df: pd.DataFrame, value: str) -> int:
        """
        Busca a primeira linha cujo conteúdo (concatenado) contenha `value`.
        A busca é flexível: ignora maiúsculas/minúsculas e espaços/accentos.
        """
        def _normalize(s: Any) -> str:
            if s is None:
                return ""
            s = str(s)
            s = re.sub(r"\s+", " ", s).strip().lower()
            # remover acentos simples
            try:
                import unicodedata
                s = "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch))
            except Exception:
                pass
            return s

        target = _normalize(value)
        for i, row in df.iterrows():
            row_text = _normalize(row.to_string())
            if target in row_text or re.search(r"\W*".join(re.escape(tok) for tok in target.split()), row_text):
                return i
        return -1

    def extract_credit_card_debits(self, html_output: str, phrase_total: str = "total da sua fatura é") -> pd.DataFrame:
        """
        Extrai tabelas de débitos do HTML gerado pelo Docling e retorna um DataFrame consolidado.
        Mantém colunas originais e adiciona coluna 'VALUE AMOUNT' com o total da fatura quando encontrada.
        """
        soup = BeautifulSoup(html_output, "html.parser")
        credit_card_amount = self._find_credit_amount(soup, phrase_total)

        tables = soup.find_all("table")
        df_list: List[pd.DataFrame] = []

        for table in tables:
            try:
                # usar StringIO para evitar FutureWarning do pandas
                table_html = str(table)
                df = pd.read_html(StringIO(table_html), keep_default_na=False)[0]
            except Exception as e:
                print("pandas.read_html falhou para uma tabela: %s", e)
                continue

            # promover primeira linha para header se necessário
            if any(isinstance(c, int) for c in df.columns):
                df.columns = df.iloc[0].astype(str).values
                df = df.iloc[1:].reset_index(drop=True)

            # normalizar nomes
            df.columns = [str(c).strip() for c in df.columns]

            if len(df.columns) < 1:
                continue

            # heurística de detecção: procura por colunas ou conteúdo que pareçam ser DATA + ESTABELECIMENTO
            cols_low = " ".join(df.columns).upper()
            if "DATA" in cols_low and "ESTABELECIMENTO" in cols_low:
                df_list.append(df)
                continue

            # senão, procurar linha que contenha cabeçalho 'DATA' e promover como header
            str_index = self._find_value_index_in_df(df, "DATA")
            if str_index != -1:
                df.columns = df.iloc[str_index]
                df = df.drop(index=range(0, str_index + 1)).reset_index(drop=True)
                df.columns = [str(c).strip() for c in df.columns]
                if "DATA" in " ".join(df.columns).upper() and "ESTABELECIMENTO" in " ".join(df.columns).upper():
                    df_list.append(df)

        if not df_list:
            print("Nenhuma tabela de transações encontrada no HTML.")

        # concatena e limpa
        df_card_debits = pd.concat(df_list, ignore_index=True, sort=False)

        # remover seções após indicadores de final de lançamentos (vários formatos)
        for marker in ("Lançamentosnocartão", "Lançamentos nocartão", "Lançamentos no cartão", "LANCAMENTOSNOCARTAO"):
            idx = self._find_value_index_in_df(df_card_debits, marker)
            if idx != -1:
                df_card_debits = df_card_debits.drop(index=range(idx, df_card_debits.shape[0])).reset_index(drop=True)

        # adicionar coluna com o valor total encontrado (se houver)
        df_card_debits["VALUE AMOUNT"] = credit_card_amount

        return df_card_debits

    def process(self, pdf_path: str | Path, password: Optional[str] = None) -> pd.DataFrame:
        """
        Processo completo: converte PDF para HTML (utilizando senha quando necessário)
        e extrai DataFrame de débitos do cartão de crédito.
        """
        try:
            result = self.convert_with_optional_password(pdf_path, password)
            document = getattr(result, "document", None)
            if document is None:
                print("Resultado da conversão não contém 'document'.")
            html_output = document.export_to_html()
            df = self.extract_credit_card_debits(html_output)
            return df
        except Exception as e:
            print("Erro inesperado no processamento: %s", e)


# service = PDFToDataFrameService()
# df = service.process(r"C:\caminho\para\arquivo.pdf", password="minha_senha")