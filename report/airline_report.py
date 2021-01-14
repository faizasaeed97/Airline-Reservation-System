# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class airline_ticket(models.TransientModel):
    _name = 'ticket.details'
    _description = "Airline Ticket Report Details"

    depart_dates = fields.Date(required=True, string="Date to Depart")
    arrival_dates = fields.Date(required=True, string="Date To Arrive")

    def get_total_val(self, air):
        dix = {}
        totalv = 0

        for rec in air:
            ticket = self.env['airline.module'].search_count(
                [('my_sequence_air', '=', rec.id), '|', ('ticket_type', '=', 'return'),
                 ('Class', '=', 'economy'), ('depart_date', '>=', self.depart_dates),
                 ('arrive_date', '<=', self.arrival_dates),
                 ])
            totalv += ticket

        dix['totl'] = totalv

        return dix

    def print_report(self):
        plist2 = []

        air2 = self.env['airline.module'].search(
            [('ticket_type', '!=', 'one way')])

        for rec in air2:
            dix = {}
            dix['data'] = 'd'
            dix['div'] = rec.ticket_type

            emps2 = self.env['airline.module'].search(
                [('departure.airport.location', '=', rec.id)])
            gettot2 = self.get_tot_val(air2)

            dix['tot'] =gettot2.get('totl')
            plist2.append(dix)
            for dec in emps2:
                ticket = self.env['airline.module'].search_count(
                    [('my_sequence_air', '=', rec.id), '|', ('ticket_type', '=', 'return'),
                     ('Class', '=', 'economy'), ('depart_date', '>=', self.depart_dates),
                     ('arrive_date', '<=', self.arrival_dates),
                     ])
                dix = {}
                dix['id'] = dec.my_sequence_air

                dix['ticket type'] = dec.ticket_type
                dix['div'] = rec.id
                dix['total'] = ticket
                dix['data'] = 'nd'
                plist2.append(dix)

        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'depart_date': self.depart_dates,
                'arrive_date': self.arrival_dates,
                'dta': plist2
            },
        }
        return self.env.ref('airline.action_report_airline_ticket').report_action(self, data=data)


class absnetscxReport(models.AbstractModel):
    _name = 'report.airline.air_ticket'
    _description = "Airline Ticket Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        date_f = data['form']['depart_date']
        date_t = data['form']['arrive_date']
        datax = data['form']['dta']

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'df': date_f,
            'dt': date_t,
            'dtax': datax,
        }


