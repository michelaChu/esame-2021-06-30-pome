from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.Localization from classification c """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Localization"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select Loc1, Loc2
                    from 
                    (select c.GeneID as GeneID1, c.Localization as Loc1, c2.GeneID as GeneID2, c2.Localization as Loc2
                    from classification c, classification c2, interactions i 
                    where c.GeneID = i.GeneID1 and c2.GeneID = i.GeneID2) as t
                    where Loc1 != Loc2
                    group by Loc1, Loc2
                    having count(*) >= 1"""

        cursor.execute(query)

        for row in cursor:
            result.append((row["Loc1"], row["Loc2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getWeight(loc1, loc2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(distinct i.`Type`) as peso
                    from classification c, classification c2, interactions i 
                    where c.GeneID = i.GeneID1 and c2.GeneID = i.GeneID2 and c.Localization != c2.Localization 
                    and ((c.Localization = %s and c2.Localization = %s) 
                    or (c2.Localization = %s and c.Localization = %s))"""

        cursor.execute(query, (loc1, loc2, loc1, loc2))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllWeights():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select Loc1, Loc2, count(distinct `Type`) as peso
                    from 
                    (select c.Localization as Loc1, c2.Localization as Loc2, i.`Type` 
                    from classification c, classification c2, interactions i 
                    where c.GeneID = i.GeneID1 and c2.GeneID = i.GeneID2
                    union 
                    select c2.Localization as Loc2, c.Localization as Loc1, i.`Type` 
                    from classification c, classification c2, interactions i 
                    where c.GeneID = i.GeneID1 and c2.GeneID = i.GeneID2) as t
                    where Loc1 < Loc2
                    group by Loc1, Loc2"""

        cursor.execute(query)

        for row in cursor:
            result.append((row["Loc1"], row["Loc2"], row["peso"]))

        cursor.close()
        conn.close()
        return result


