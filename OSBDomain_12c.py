#=======================================================================================
# This is an example of a simple WLST offline configuration script. The script creates 
# a simple OSB 12c domain 
#
# Usage: 
#      MW_HOME/oracle_common/common/bin/wlst.sh <WLST_script> 
#
# Where: 
#      MW_HOME is MW home location.
#      <WLST_script> specifies the full path to the WLST script.
#=======================================================================================

#Database Configuration Properties
OSB_REPOS_DBURL = 'jdbc:oracle:thin:@mutsubra-pc790:1521/muthu'
OSB_REPOS_DB_PASSWORD = 'weblogic'
OSB_REPOS_DBUSER_PREFIX = 'SOA12CT'

#Admin Server Configuration properties
ADMIN_SERVER_HOST = 'mutsubra-pc7010'
ADMIN_SERVER_PORT = 7001

#SOA Server Configuration properties
OSB_SERVER_HOST = 'mutsubra-pc7010'
OSB_SERVER_PORT = 8001


#Folder Locations 
MW_HOME = '/muthu/SOA/SOA12CF'
DOMAIN_HOME = '/muthu/SOA/SOA12CF/user_projects/domains/OSB_Domain_WLST'


def changeDatasourceToXA(datasource):
  print '>>>>>>> Change datasource '+datasource
  cd('/')
  cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDriverParams/NO_NAME_0')
  set('DriverName','oracle.jdbc.xa.client.OracleXADataSource')
  set('UseXADataSourceInterface','True') 
  cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDataSourceParams/NO_NAME_0')
  set('GlobalTransactionsProtocol','TwoPhaseCommit')
  cd('/')

#=======================================================================================
# Open a domain template.
#=======================================================================================

readTemplate(MW_HOME+'/wlserver/common/templates/wls/wls.jar')

#=======================================================================================
# Configure the Administration Server and SSL port.
#
# To enable access by both local and remote processes, you should not set the 
# listen address for the server instance (that is, it should be left blank or not set). 
# In this case, the server instance will determine the address of the machine and 
# listen on it. 
#=======================================================================================

cd('Servers/AdminServer')
set('ListenAddress', ADMIN_SERVER_HOST)
set('ListenPort', ADMIN_SERVER_PORT)

#=======================================================================================
# Define the user password for weblogic.
#=======================================================================================

cd('/')
cd('Security/base_domain/User/weblogic')
cmo.setPassword('welcome1')

#=======================================================================================
# Write the domain and close the domain template.
#=======================================================================================

setOption('OverwriteDomain', 'true')

#Creating default coherence cluster
create('defaultCoherenceCluster', 'CoherenceClusterSystemResource')

cd('/')
create('osb_server1', 'Server')
cd('Server/osb_server1')
set('ListenPort', OSB_SERVER_PORT) 
set('ListenAddress', OSB_SERVER_HOST)
set('CoherenceClusterSystemResource', 'defaultCoherenceCluster')

#assigning target for default coherence cluster
cd('/')
assign('Server','osb_server1','CoherenceClusterSystemResource','defaultCoherenceCluster')

cd('/CoherenceClusterSystemResource/defaultCoherenceCluster')
set('Target', 'osb_server1')

print ">>>>>>> Creating WLS Domain"

writeDomain(DOMAIN_HOME)

closeTemplate()


#=======================================================================================
# Exit WLST.
#=======================================================================================

print ">>>>>>> Extending the domain for OSB"
readDomain(DOMAIN_HOME)

print ">>>>>>> Adding Webservice Template"
addTemplate(MW_HOME+'/oracle_common/common/templates/wls/oracle.wls-webservice-template_12.1.3.jar')

print ">>>>>>> Adding OSB Template"
addTemplate(MW_HOME+'/osb/common/templates/wls/oracle.osb_template_12.1.3.jar')

print '>>>>>>> Datasources Change Start'
print '>>>>>>> Change datasource LocalScvTblDataSource'

cd('/JDBCSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource/JDBCDriverParams/NO_NAME_0')
set('URL',OSB_REPOS_DBURL)
cmo.setPasswordEncrypted(OSB_REPOS_DB_PASSWORD)
cd('Properties/NO_NAME_0/Property/user')
set('Value',OSB_REPOS_DBUSER_PREFIX+'_STB')

print '>>>>>>> Call getDatabaseDefaults to read details from service table'
getDatabaseDefaults()    

#changeDatasourceToXA('EDNDataSource')
changeDatasourceToXA('OraSDPMDataSource')
changeDatasourceToXA('SOADataSource')

print '>>>>>>> Datasources Change End'

print '>>>>>>> Add server groups to AdminServer'
serverGroup = ["WSM-CACHE-SVR" , "WSMPM-MAN-SVR" , "JRF-MAN-SVR"]
setServerGroups('AdminServer', serverGroup)   

print '>>>>>>> Add server group(s) to osb_server1'
serverGroup = ["OSB-MGD-SVRS-COMBINED"]
setServerGroups('osb_server1', serverGroup)    

print '>>>>>>> Update Domain....... Please wait.. takes little time to populate OPSS Schema'
updateDomain()

print '>>>>>>> Update Domain Completed'

closeDomain()

print '>>>>>>> Domain Creation Completed'

exit()
