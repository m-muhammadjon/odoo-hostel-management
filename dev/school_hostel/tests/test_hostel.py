# See LICENSE file for full copyright and licensing details.

from odoo import fields
from odoo.tests import common


class TestHostel(common.TransactionCase):
    def setUp(self):
        super(TestHostel, self).setUp()
        self.hostel_type_obj = self.env["hostel.type"]
        self.hostel_room_obj = self.env["hostel.room"]
        self.hostel_student_obj = self.env["hostel.student"]
        self.student = self.env.ref("school.demo_student_student_7")
        self.res_partner = self.env["res.partner"]
        # create hostel rector
        self.rector = self.res_partner.create(
            {
                "name": "Hostel Rector",
                "is_hostel_rector": True,
                "email": "hostelrec@demo.com",
            }
        )
        #        Create Hostel Type
        self.hostel_type = self.hostel_type_obj.create(
            {"name": "Test Hostel", "type": "female", "rector": self.rector.id}
        )
        #        Create Hostel Room
        self.hostel_room = self.hostel_room_obj.create(
            {
                "name": self.hostel_type.id,
                "room_no": "101",
                "student_per_room": "3",
                "rent_amount": 1000,
            }
        )
        self.hostel_room._compute_check_availability()
        #        Create Hostel Student
        current_date = fields.datetime.today()
        self.hostel_student = self.hostel_student_obj.create(
            {
                "student_id": self.student.id,
                "hostel_info_id": self.hostel_type.id,
                "room_id": self.hostel_room.id,
                "admission_date": current_date,
                "duration": 2,
            }
        )
        self.hostel_student.check_duration()
        self.hostel_student._compute_remaining_fee_amt()
        self.hostel_student._compute_rent()
        self.hostel_student._get_hostel_user()
        self.hostel_student.reservation_state()
        self.hostel_student.onchnage_discharge_date()
        self.hostel_student.discharge_state()
        self.hostel_student.student_expire()
        self.hostel_student.print_fee_receipt()

    def test_hostel(self):
        self.assertEqual(self.student.state, "done")
        self.assertIn(self.hostel_room.name, self.hostel_type)
