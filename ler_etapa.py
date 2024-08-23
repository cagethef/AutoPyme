import ezodf as doc

path = 'utils/EtapasDesenv_AutoPyme.ods'
archive = doc.opendoc(path)
sheet = archive.sheets[0]

def load_etapas_from_ods():     # Carregar ETAPAS
    etapas = []
    for row in sheet.rows():
        etapa_value = row[0].value
        if etapa_value == None:
            break
        else:
            etapas.append(etapa_value)
    return etapas

def search_workstation_from_ods(my_work):
    workstation = None
    for row in sheet.rows():
        etapa_value = row[0].value
        if etapa_value == my_work:
            workstation = row[1].value
        elif etapa_value == None:
            break
    return workstation

def load_workstation_from_ods():     # Carregar ESTACAO TRABALHO
    workstations = []
    for row in sheet.rows():
        workstation_value = row[1].value
        if workstation_value == None:
            break
        else:
            workstations.append(workstation_value)
    return workstations

def load_desc_from_ods(): # CARREGAR DESCRICAO ETAPAS
    valores = []
    for row in sheet.rows():
        descricao_value = row[2].value
        if descricao_value == None:
            break
        else:
            valores.append(descricao_value)
    return valores

def load_full_from_ods():     # Carregar dados da planilha  
    work = []
    for row in sheet.rows():
        etapa_value = row[0].value
        descricao_value = row[2].value
        if etapa_value == None or descricao_value == None:
            break
        else:
            etapa_str = str(etapa_value).replace('(', '').replace(')', '').replace("'", '')
            descricao_str = str(descricao_value).replace('(', '').replace(')', '').replace("'", '')
            work.append(f"{etapa_str},{descricao_str}")
    return work

#print(load_full_from_ods())

