from ..elementTypes import htmEl, table
from ..Element import Element as ele

class Table(table, htmEl):

    def __init__(self, header = [], body = {}, footer={}, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        
        if header:
            self.add(
                ele('thead').add(
                    ele('tr').add(
                        (ele('th', _) for _ in header)
                    )
                )
            )
        if body:
            self.add(
                ele('tbody').add(
                    (ele('tr').add(
                        ele('th', label),
                        ele('td', value)
                    ) for label,value  in body.items())
                )
            )
                
