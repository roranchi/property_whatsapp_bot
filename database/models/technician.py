from database.connection import get_connection

class Technician:
    def __init__(self, id=None, name=None, phone=None, specialty=None, active=True):
        self.id = id
        self.name = name
        self.phone = phone
        self.specialty = specialty
        self.active = active
    
    @staticmethod
    def get_by_specialty(specialty):
        """الحصول على فني حسب التخصص"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, phone, specialty, active
            FROM technicians 
            WHERE specialty = ? AND active = 1
            ORDER BY RANDOM()
            LIMIT 1
        ''', (specialty,))
        
        tech_data = cursor.fetchone()
        conn.close()
        
        if tech_data:
            return Technician(
                id=tech_data['id'],
                name=tech_data['name'],
                phone=tech_data['phone'],
                specialty=tech_data['specialty'],
                active=tech_data['active']
            )
        return None
    
    @staticmethod
    def get_all_active():
        """الحصول على جميع الفنيين النشطين"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, phone, specialty, active
            FROM technicians 
            WHERE active = 1
            ORDER BY specialty, name
        ''')
        
        technicians = []
        for tech_data in cursor.fetchall():
            technicians.append(Technician(
                id=tech_data['id'],
                name=tech_data['name'],
                phone=tech_data['phone'],
                specialty=tech_data['specialty'],
                active=tech_data['active']
            ))
        
        conn.close()
        return technicians
    
    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'specialty': self.specialty,
            'active': self.active
        }
