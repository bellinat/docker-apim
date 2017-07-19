import xml.etree.ElementTree as ET

ip_port_mysql = input('Digite o IP e a porta do servidor mysql <127.0.0.1:3306>: ') or '192.168.190.97:3306'
username_database = input('Digite o usuário do banco de dados: ') or 'root'
password_database = input('Digite a senha do banco de dados: ') or 'root'

datasource_gateway_manager_path = './gateway-manager/carbon/repository/conf/datasources/master-datasources.xml'
datasource_gateway_worker_path = './gateway-worker/carbon/repository/conf/datasources/master-datasources.xml'
datasource_keymanager_path = './keymanager/carbon/repository/conf/datasources/master-datasources.xml'
datasource_publisher_store_path = './publisher-store/carbon/repository/conf/datasources/master-datasources.xml'
datasource_traffic_manager_path = './traffic-manager/carbon/repository/conf/datasources/master-datasources.xml'
datasource_apim = {'WSO2AM_DB': 'jdbc:mysql://{}/apimgtdb?autoReconnect=true',
                        'WSO2UM_DB': 'jdbc:mysql://{}/userdb?autoReconnect=true', 
                        'WSO2REG_DB': 'jdbc:mysql://{}/regdb?autoReconnect=true' }


datasource_analytics_master_path = './am-analytics/carbon/repository/conf/datasources/analytics-datasources.xml'
datasource_analytics = { 'WSO2_ANALYTICS_EVENT_STORE_DB': 'jdbc:mysql://{}/stats_db?autoReconnect=true&amp;relaxAutoCommit=true',
                            'WSO2_ANALYTICS_PROCESSED_DATA_STORE_DB': 'jdbc:mysql://{}/stats_db?autoReconnect=true&amp;relaxAutoCommit=true'}


datasource_analytics_stats_path = './am-analytics/carbon/repository/conf/datasources/stats-datasources.xml'
datasource_stats_analytics = {'WSO2AM_STATS_DB': 'jdbc:mysql://{}/stats_db?autoReconnect=true&amp;relaxAutoCommit=true'}


def set_database_connection(**kwargs):
    datasource_names = kwargs['datasource_names']
    xml_path = kwargs['xml_path']
    ip_port_mysql_database = kwargs['ip_port_mysql_database']
    username = kwargs['username_database']
    password = kwargs['password_database']

    tree = ET.parse(xml_path)
    root = tree.getroot()

    for datasource in [ i for i in root.find('datasources').findall('datasource') if i.find('name').text in datasource_names]:
        datasource_name = datasource.find('name').text

        print('File = {} [{}]. Changing connection string.'.format(xml_path, datasource_name))
        datasource.find('definition').find('configuration').find('url').text = datasource_names[datasource_name].format(ip_port_mysql_database)

        print('File = {} [{}]. Changing database username.'.format(xml_path, datasource_name))
        datasource.find('definition').find('configuration').find('username').text = username
        
        print('File = {} [{}]. Changing database password.'.format(xml_path, datasource_name))
        datasource.find('definition').find('configuration').find('password').text = password

    tree.write(xml_path)


def set_cacheId_registry(**kwargs):
    xml_path = kwargs['xml_path']
    cache_id = kwargs['cache_id']
    tree = ET.parse(xml_path)
    root = tree.getroot()
    print('File = {} [{}]. Changing cacheId.'.format(xml_path,'cacheId'))
    remote_instance = root.find('remoteInstance').find('cacheId').text = cache_id
    tree.write(xml_path)

xml_path =  './publisher-store/carbon/repository/conf/registry.xml'
cacheId = '{}@jdbc:mysql://{}/regdb'.format(username_database, ip_port_mysql)




set_database_connection(username_database=username_database, password_database=password_database, datasource_names=datasource_apim,xml_path=datasource_gateway_manager_path,ip_port_mysql_database=ip_port_mysql)
set_database_connection(username_database=username_database, password_database=password_database, datasource_names=datasource_apim,xml_path=datasource_traffic_manager_path,ip_port_mysql_database=ip_port_mysql)
set_database_connection(username_database=username_database, password_database=password_database, datasource_names=datasource_apim,xml_path=datasource_gateway_worker_path,ip_port_mysql_database=ip_port_mysql)
set_database_connection(username_database=username_database, password_database=password_database, datasource_names=datasource_apim,xml_path=datasource_keymanager_path,ip_port_mysql_database=ip_port_mysql)
set_database_connection(username_database=username_database, password_database=password_database, datasource_names=datasource_apim,xml_path=datasource_publisher_store_path,ip_port_mysql_database=ip_port_mysql)
set_database_connection(username_database=username_database, password_database=password_database, datasource_names=datasource_analytics,xml_path=datasource_analytics_master_path,ip_port_mysql_database=ip_port_mysql)
set_database_connection(username_database=username_database, password_database=password_database, datasource_names=datasource_stats_analytics,xml_path=datasource_analytics_stats_path,ip_port_mysql_database=ip_port_mysql)
set_cacheId_registry(xml_path=xml_path, cache_id=cacheId)