from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from typing import List
from pydantic import Required, create_model
model = ''
excluded = []

for each_col in  model.__table__._columns:
            if each_col.name not in excluded:
                if each_col.default:
                    f_def = each_col.default.arg
                else:
                    f_def = Required

                # if isinstance(each_col.type, Integer):
                _type = each_col.type.python_type