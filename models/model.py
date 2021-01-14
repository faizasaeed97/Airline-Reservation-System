from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
import datetime as dt
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


# from sales_customization.models import sale_order


class airline_reservation(models.Model):
    _name = 'airline.module'
    _rec_name = 'my_sequence_air'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    my_sequence_air = fields.Char(string="ID Number")
    partner_id = fields.Many2one('res.partner', string='Customer ID')
    customer_name = fields.Char(string="Name of Customer")
    ticket_type = fields.Selection([('return', 'Return'), ('one way', 'One way'), ('multi_city', 'Multi-City')],
                                   string="Ticket Type", required=True, default='return')
    departure_airport = fields.Many2one('departure.airport', string=" Departure Airport", required=True)
    arrival_airport = fields.Many2one('arrival.airport', string=" Arrival Airport", required=True)
    depart_date = fields.Date(String="Departure Date")
    arrive_date = fields.Date(String="Arrival Date")
    Class = fields.Selection([('economy', 'Economy'), ('first', 'First'), ('bussiness', 'Bussiness')],
                             string="Ticket Type", required=True, default='economy')
    my_dates = fields.Boolean(string="My dates are flexible (+/- 3 days)", default=False)
    passengers_details = fields.One2many('passengers.details', 'passenger_id', string="Passengers:")
    add_city = fields.One2many('multi.details', 'trip_id', string="Add Another City:")
    Billing_type = fields.Integer(string=" Cost according to ticket type")
    mul = fields.Float(string=" Cost according to ticket type", default=1)
    total_cost = fields.Float(string="Total Bill")
    date_of_booking = fields.Date(string=" Date of booking")

    @api.onchange('ticket_type')
    def get_billing_type(self):
        for rec in self:

            if rec.ticket_type == 'return':
                rec.Billing_type = 2
            if rec.ticket_type == 'multi_city':
                rec.Billing_type = 'multi.details.trip_id'

            else:
                rec.Billing_type = 1

    @api.onchange('Class')
    def get_class_bill_type(self):
        for rec in self:

            if rec.Class == 'economy':
                mul = 1 + rec.Billing_type
            if rec.Class == 'first':
                mul = rec.Billing_type + 2
            else:
                mul = rec.Billing_type + 3

    @api.onchange('passengers_details', 'passenger_age')
    def get_no_persons(self):
        if self.passengers_details:
            total_cost = 0.0
            for rec in self.passengers_details:

                if rec.adults_count > 0:
                    total_cost += (rec.adults_count * 160000) * self.mul
                if rec.children_count > 0:
                    total_cost += (rec.children_count * 45000) * self.mul

                else:
                    total_cost += (rec.infant_count * 21000) * self.mul

            self.total_cost = total_cost

    # total_passengers = fields.Integer(String=" Total person")

    # passengers_details.get_no_persons()

    # class_type_cost = fields.Integer (string= "Cost number")

    # self.pool.get('airline_obj').get_no_persons

    # @api.onchange('ticket_type')
    # def total_bill(self):
    #     for rec in self:
    #
    #         dis = rec.discount / 100
    #         rec.price_after = rec.price_subtotal * dis

    # @api.depends('ticket_type')
    # def get_billing_type(self):
    #     for rec in self:
    #
    #         if rec.ticket_type == 'return':
    #             rec.Billing_type= 2
    #         if rec.ticket_type == 'multi_city':
    #             rec.Billing_type = rec.id
    #
    #         else:
    #             rec.Billing_type = 1

    @api.model
    def create(self, vals_list):

        name = self.env['ir.sequence'].next_by_code('airline.auto.generate.sequence')
        vals_list['my_sequence_air'] = name
        templates = super(airline_reservation, self).create(vals_list)
        return templates

    def create_sale_order(self):
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'note': 'Invoice after delivery',

        })
        for rec in self.passengers_details:
            airline_product = self.env['product.product'].search([('product_tmpl_id', '=', rec.type_passenger.id)])
            # rec.airline_product = rec.product_id_air
            air_sale_order_line = rec.env['sale.order.line'].create({
                'product_id': airline_product.id,
                'name': rec.passenger_name,
                'product_uom_qty': 1,
                'price_unit': rec.unit_price,
                'order_id': sale_order.id,
                # 'price_subtotal': rec.Total_price,
            })
            # product_tmpl_id = rec.type_passenger.id






class Departure(models.Model):
    _name = 'departure.airport'
    _rec_name = 'location'

    dep_airport_name = fields.Char(String=" Departure Airport Name")
    location = fields.Char(string="Country")
    city = fields.Char(string="City")


class Arrival(models.Model):
    _name = 'arrival.airport'
    _rec_name = 'a_location'

    arrival_airport_name = fields.Char(String="Arrival Airport Name")
    a_location = fields.Char(string="Country")
    a_city = fields.Char(string="City")


class passengers_details(models.Model):
    _name = 'passengers.details'

    passenger_id = fields.Many2one('airline.module', string="Passenger ID")
    passenger_name = fields.Char(string="Name of Passenger")
    partner_id = fields.Many2one('res.partner', string='Customer ID')
    passenger_age = fields.Integer(string="age")
    type_passenger = fields.Many2one('product.template', string="Passenger Type")
    qty_of_passenger = fields.Integer(string="No. of passenger", default=1)
    unit_price = fields.Integer(string="Ticket price")
    Total_price = fields.Float(string="Total Amount")
    adults_count = fields.Integer(string="Number of Adutls (Ages 12+)")
    children_count = fields.Integer(string="Number of Children (Ages 2-11)")
    infant_count = fields.Integer(string="Number of Infants (Ages under 2)")
    # product_id_air = fields.Char(string="ID")

    # Class_bill = fields.Integer (string = "Class calculate")

    @api.onchange('qty_of_passenger', 'unit_price')
    def total_calculate(self):
        for rec in self:
            rec.Total_price = rec.unit_price * rec.qty_of_passenger

    # def line_of_item(self):
    #     air_sale_order_line = self.env['sale.order.line'].create({
    #         'order_id': self.sale_order.id,
    #         'name': self.product_id.name,
    #         'product_id': self.airline_product.id,
    #         'product_uom_qty': 1,
    #         'qty_delivered': 1,
    #         'product_uom': self.product_id.partner_id.id,
    #         'price_unit': self.product_id.unit_price,
    #         'order_id': self.sale_order.id,
    #         'price_subtotal': self.product_id.Total_price,
    #     })
        # return air_sale_order_line

    @api.onchange('passenger_name')
    def age_assign(self):
        for rec in self:
            if rec.passenger_name:
                adults_count = 0.0
                children_count = 0.0
                infant_count = 0.0
                if rec.passenger_age >= 12:
                    adults_count += 1
                if rec.passenger_age > 2 and rec.passenger_age < 12:
                    children_count += 1

                else:
                    infant_count += 1

                rec.adults_count = adults_count
                rec.children_count = children_count
                rec.infant_count = infant_count


class add_city2(models.Model):
    _name = 'multi.details'

    departure_airport2 = fields.Many2one('departure.airport2', string=" Departure Airport", required=True)
    arrival_airport2 = fields.Many2one('arrival.airport2', string=" Arrival Airport", required=True)
    departure_date = fields.Date(String="Departure Date")
    trip_id = fields.Many2one('airline.module', string="Trip ID")


class Departure2(models.Model):
    _name = 'departure.airport2'
    _rec_name = 'location2'

    dep_airport_name2 = fields.Char(String=" Departure Airport Name")
    location2 = fields.Char(string="Country")
    city2 = fields.Char(string="City")


class Arrival2(models.Model):
    _name = 'arrival.airport2'
    _rec_name = 'a_location2'

    arrival_airport_name2 = fields.Char(String="Arrival Airport Name")
    a_location2 = fields.Char(string="Country")
    a_city2 = fields.Char(string="City")
