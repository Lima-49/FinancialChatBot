from flask import Blueprint, request

clientBp = Blueprint('HistoricoFinanceiroController', __name__)

@clientBp.route('/historico-financeiro', methods=['POST'])
def get_finacial_hist():
    result = 'oi'