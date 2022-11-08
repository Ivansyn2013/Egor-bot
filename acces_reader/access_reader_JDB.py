import jaydebeapi

db_path = "1.accdb"

if __name__ == '__main__':

    ucanaccess_jars = [
        "/UCanAccess-5.0.1.bin/ucanaccess-5.0.1.jar",
        "/UCanAccess-5.0.1.bin/lib/commons-lang3-3.8.1.jar",
        "/UCanAccess-5.0.1.bin/lib/commons-logging-1.2.jar",
        "/UCanAccess-5.0.1.bin/lib/hsqldb-2.5.0.jar",
        "/UCanAccess-5.0.1.bin/lib/jackcess-3.0.1.jar",
    ]


classpath = ":".join(ucanaccess_jars)
cnxn = jaydebeapi.connect(
    "net.ucanaccess.jdbc.UcanaccessDriver",
    f"jdbc:ucanaccess://{db_path};newDatabaseVersion=V2010",
    ["", ""],
    classpath
    )
crsr = cnxn.cursor()
try:
    crsr.execute("DROP TABLE table1")
    cnxn.commit()
except jaydebeapi.DatabaseError as de:
    print(de)