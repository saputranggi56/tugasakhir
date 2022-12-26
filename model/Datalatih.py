

import psycopg2
import psycopg2.extras



class Datalatih():
    
    def __init__(self, storage="" ):
        self.storage = storage
    
    def getData(self):
        cur = self.storage.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = "SELECT * FROM flagging_kalimat"
        cur.execute(s)
        data = cur.fetchall()

        return data

    def getDataUji(self):
        cur = self.storage.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = "SELECT * FROM data_uji"
        cur.execute(s)
        data = cur.fetchall()

        return data

    def getDataByLabel(self, flagging=''):
        cur = self.storage.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = "SELECT after_praproses FROM data_uji WHERE flagging = '"+flagging+"'"
        cur.execute(s)
        data = cur.fetchall()

        return data

    def getDataPercentage(self, portal=''):
        cur = self.storage.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if portal:
            s = """SELECT 
                    *,
                    ROUND(CAST( ((total_positif::float/total::float) * 100::FLOAT ) as numeric ) ,2) as per_positif,
                    ROUND(CAST( ((total_negatif::float/total::float) * 100::FLOAT ) as numeric ) ,2) as per_negatif,
                    ROUND(CAST( ((total_netral::float/total::float) * 100::FLOAT ) as numeric ) ,2) as per_netral

                FROM 
                    (
                    SELECT 
                        COUNT(*) as total, 
                        COUNT(*) FILTER (WHERE flagging = '0') as total_netral,
                        COUNT(*) FILTER (WHERE flagging = '1') as total_positif, 
                        COUNT(*) FILTER (WHERE flagging = '2') as total_negatif
                    FROM 
                        data_uji 
                    WHERE 
                        portal = '"""+portal+"""'

                    ) x;
                """
        else:
             s = """SELECT 
                    *,
                    ROUND(CAST( ((total_positif::float/total::float) * 100::FLOAT ) as numeric ) ,2) as per_positif,
                    ROUND(CAST( ((total_negatif::float/total::float) * 100::FLOAT ) as numeric ) ,2) as per_negatif,
                    ROUND(CAST( ((total_netral::float/total::float) * 100::FLOAT ) as numeric ) ,2) as per_netral

                FROM 
                    (
                    SELECT 
                        COUNT(*) as total, 
                        COUNT(*) FILTER (WHERE flagging = '0') as total_netral,
                        COUNT(*) FILTER (WHERE flagging = '1') as total_positif, 
                        COUNT(*) FILTER (WHERE flagging = '2') as total_negatif
                    FROM 
                        data_uji 
                    ) x;
                """
        cur.execute(s)
        data = cur.fetchall()

        return data
    def getDataByLabelAndWord(self, flagging='', word=''):
        cur = self.storage.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = "SELECT after_praproses FROM data_uji WHERE flagging = '"+flagging+"' AND after_praproses ilike '%"+word+"%'"
        cur.execute(s)
        data = cur.fetchall()

        return data

    def getAllDataByClass(self, flagging = '', portal=''):
        cur = self.storage.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = """SELECT 
                url, 
                portal, 
                judul, 
                publis_date, 
                kalimat, 
                flagging, 
                berita_id  
            FROM 
                data_uji 
            WHERE 
                flagging = '"""+flagging+"""'"""

        if portal == 'ALL':
            s+= """ """
        else:
            s+= """ AND portal = '"""+portal+"""'"""
            

        s+= """ ORDER BY 
                portal,
                url,
                berita_id"""
        cur.execute(s)
        data = cur.fetchall()

        return data

    def getDataBeritaById(self, berita_id = ''):
        cur = self.storage.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = "SELECT * FROM data_uji WHERE berita_id = '"+berita_id+"'"
        cur.execute(s)
        data = cur.fetchall()

        return data

    def getDataBySentence(self, sentence = '', p_portal="" ,p_class=""):
        cur = self.storage.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = """
                SELECT 
                    url, 
                    portal, 
                    judul, 
                    after_praproses, 
                    flagging,
                    berita_id
                FROM 
                    data_uji 
                WHERE 
                    after_praproses like '%"""+sentence+"%'"""
        
        if p_portal != 'all':
            s+= """ AND portal = '"""+p_portal+"""'"""
        
        if p_class != 'all':
            s+= """ AND flagging = '"""+p_class+"""'"""
        
       
        

        cur.execute(s)
        data = cur.fetchall()

        return data