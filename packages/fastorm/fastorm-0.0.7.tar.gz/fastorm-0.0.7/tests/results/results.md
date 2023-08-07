```bash
export PYTHONPATH="$(realpath .):$(realpath ./tests) $(pyenv which python) && cd tests && run_tests.py ; cd ..
```


# Tests
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94mfastorm.match_type:[39m [0m
[90m[7m        [27m[39m [90mCould not parse as a single type list (e.g. INT[][]), now will be a json field.[39m[49m[0m
[90m[7m        [27m[39m [90mTraceback (most recent call last):[39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1276, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    subtype_is_optional, sql_type = cls.match_type([39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1242, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    raise e[39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1233, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    _, sql_type = cls.match_type([39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1209, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    raise TypeError([39m[49m[0m
[90m[7m        [27m[39m [90mTypeError: ('Union with more than one type at key None.', (<class 'str'>, <class 'int'>))[39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94mfastorm.match_type:[39m [0m
[90m[7m        [27m[39m [90mCould not parse as a single type list (e.g. INT[][]), now will be a json field.[39m[49m[0m
[90m[7m        [27m[39m [90mTraceback (most recent call last):[39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1276, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    subtype_is_optional, sql_type = cls.match_type([39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1242, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    raise e[39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1233, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    _, sql_type = cls.match_type([39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1209, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    raise TypeError([39m[49m[0m
[90m[7m        [27m[39m [90mTypeError: ('Union with more than one type at key None.', (<class 'str'>, <class 'int'>))[39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94mfastorm.match_type:[39m [0m
[90m[7m        [27m[39m [90mCould not parse as a single type list (e.g. INT[][]), now will be a json field.[39m[49m[0m
[90m[7m        [27m[39m [90mTraceback (most recent call last):[39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1233, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    _, sql_type = cls.match_type([39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1242, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    raise e[39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1233, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    _, sql_type = cls.match_type([39m[49m[0m
[90m[7m        [27m[39m [90m  File "/Users/luckydonald/Documents/programming/Python/fastORM/fastorm/__init__.py", line 1209, in match_type[39m[49m[0m
[90m[7m        [27m[39m [90m    raise TypeError([39m[49m[0m
[90m[7m        [27m[39m [90mTypeError: ('Union with more than one type at key None.', (<class 'str'>, <class 'int'>))[39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94masyncio.__init__:[39m [90mUsing selector: KqueueSelector[39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94masyncio.close:[39m [90mClose <_UnixSelectorEventLoop running=False closed=False debug=True>[39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94masyncio.__init__:[39m [90mUsing selector: KqueueSelector[39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94masyncio.close:[39m [90mClose <_UnixSelectorEventLoop running=False closed=False debug=True>[39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94masyncio.__init__:[39m [90mUsing selector: KqueueSelector[39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94masyncio.close:[39m [90mClose <_UnixSelectorEventLoop running=False closed=False debug=True>[39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94masyncio.__init__:[39m [90mUsing selector: KqueueSelector[39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94masyncio.close:[39m [90mClose <_UnixSelectorEventLoop running=False closed=False debug=True>[39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94mfastorm.build_sql_delete:[39m [90mFields to DELETE for selector ['"id_part_1" = $1', '"id_part_2" = $2']: [12, 'banana'][39m[49m[0m
[90m[7mDEBUG   [27m[90m 2021-11-02 13:56:53[39m[94m [94mfastorm.build_sql_update:[39m [90mFields to UPDATE for selector ['"id_part_1" = $2', '"id_part_2" = $3']: {'foo': 69.42}[39m[49m[0m
              Unit Test Report
[0;0;36mStatus: [0;0m
    [0;0;32mPass:[0;0m 41

[0;0;36mDescription:[0;0m
[0;0;36mSummary: [0;0m
                                                               Test group/Test case                                                               | Count | Pass | Fail | Error
------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ---- | ---- | -----
[`test_create_table.CreateTableTestCase`](#test_create_table.CreateTableTestCase)                                                                 | 4     | 4    | 0    | 0    
[`test_create_table_online.CreateTableOnlineTestCase`](#test_create_table_online.CreateTableOnlineTestCase)                                       | 4     | 4    | 0    | 0    
[`test_delete_row.UpdateRowTestCase`](#test_delete_row.UpdateRowTestCase)                                                                         | 1     | 1    | 0    | 0    
[`doctest.DocTestCase`](#doctest.DocTestCase)                                                                                                     | 4     | 4    | 0    | 0    
[`test_get_fields.MyTestCase`](#test_get_fields.MyTestCase)                                                                                       | 2     | 2    | 0    | 0    
[`test_get_fields_references.GetFieldsReferencesMultiLayerReferenceTest`](#test_get_fields_references.GetFieldsReferencesMultiLayerReferenceTest) | 2     | 2    | 0    | 0    
[`test_get_fields_references.GetFieldsReferencesSimpleTest`](#test_get_fields_references.GetFieldsReferencesSimpleTest)                           | 4     | 4    | 0    | 0    
[`test_get_fields_references.GetFieldsReferencesSingleReferenceTest`](#test_get_fields_references.GetFieldsReferencesSingleReferenceTest)         | 6     | 6    | 0    | 0    
[`test_get_fields_typehints.GetFieldsReferencesSimpleTest`](#test_get_fields_typehints.GetFieldsReferencesSimpleTest)                             | 1     | 1    | 0    | 0    
[`test_insert_row.InsertRowTestCase`](#test_insert_row.InsertRowTestCase)                                                                         | 1     | 1    | 0    | 0    
[`test_select_row.SelectRowTestCase`](#test_select_row.SelectRowTestCase)                                                                         | 2     | 2    | 0    | 0    
[`test_table_metadata.TableMetadataTestCase`](#test_table_metadata.TableMetadataTestCase)                                                         | 5     | 5    | 0    | 0    
[`test_table_references.CreateTableTestCase`](#test_table_references.CreateTableTestCase)                                                         | 4     | 4    | 0    | 0    
[`test_update_row.UpdateRowTestCase`](#test_update_row.UpdateRowTestCase)                                                                         | 1     | 1    | 0    | 0    
Total                                                                                                                                             | 41    | 41   | 0    | 0    


### `test_create_table.CreateTableTestCase` <a name="test_create_table.CreateTableTestCase" />

                                            Test name                                             | Status |                                                                                                                                                                        Stack                                                                                                                                                                       
------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_TYPES_mapping_subclass_shadowing: if you have `class A(object): pass` and `class B(A): pass` | ✅ pass             |                                                                                                                                                                                                                                                                                                                                                    
test_sql_text                                                                                     | ✅ pass             |                                                                                                                                                                                                                                                                                                                                                    
test_type_detection_pydantic                                                                      | ✅ pass             | t0_id , FieldTypehint(is_primary_key=True, types=[FieldItem(field='t0_id', type_=ModelField(name='t0_id', type=int, required=False, default_factory='<function fastorm.Autoincrement>'))]) , ExpectedResult(is_optional=False, sql_type='BIGINT', default=PydanticUndefined)                                                                       
                                                                                                  |        | t1_1 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t1_1', type_=ModelField(name='t1_1', type=str, required=True))]) , ExpectedResult(is_optional=False, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                
                                                                                                  |        | t1_2 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t1_2', type_=ModelField(name='t1_2', type=str, required=True))]) , ExpectedResult(is_optional=False, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                
                                                                                                  |        | t1_3 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t1_3', type_=ModelField(name='t1_3', type=str, required=True))]) , ExpectedResult(is_optional=False, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                
                                                                                                  |        | t1_4 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t1_4', type_=ModelField(name='t1_4', type=str, required=True))]) , ExpectedResult(is_optional=False, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                
                                                                                                  |        | t2_1 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t2_1', type_=ModelField(name='t2_1', type=Optional[str], required=False, default=None))]) , ExpectedResult(is_optional=True, sql_type='TEXT', default=PydanticUndefined)                                                                                                        
                                                                                                  |        | t2_4 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t2_4', type_=ModelField(name='t2_4', type=Optional[str], required=False, default=None))]) , ExpectedResult(is_optional=True, sql_type='TEXT', default=PydanticUndefined)                                                                                                        
                                                                                                  |        | t2_5 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t2_5', type_=ModelField(name='t2_5', type=Optional[str], required=False, default=None))]) , ExpectedResult(is_optional=True, sql_type='TEXT', default=PydanticUndefined)                                                                                                        
                                                                                                  |        | t2_6 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t2_6', type_=ModelField(name='t2_6', type=Optional[str], required=False, default=None))]) , ExpectedResult(is_optional=True, sql_type='TEXT', default=PydanticUndefined)                                                                                                        
                                                                                                  |        | t3_1 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t3_1', type_=ModelField(name='t3_1', type=str, required=True))]) , ExpectedResult(is_optional=False, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                
                                                                                                  |        | t3_2 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t3_2', type_=ModelField(name='t3_2', type=int, required=True))]) , ExpectedResult(is_optional=False, sql_type='BIGINT', default=PydanticUndefined)                                                                                                                              
                                                                                                  |        | t3_3 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t3_3', type_=ModelField(name='t3_3', type=float, required=True))]) , ExpectedResult(is_optional=False, sql_type='DOUBLE PRECISION', default=PydanticUndefined)                                                                                                                  
                                                                                                  |        | t3_4 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t3_4', type_=ModelField(name='t3_4', type=bool, required=True))]) , ExpectedResult(is_optional=False, sql_type='BOOLEAN', default=PydanticUndefined)                                                                                                                            
                                                                                                  |        | t5_1 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t5_1', type_=ModelField(name='t5_1', type=datetime, required=True))]) , ExpectedResult(is_optional=False, sql_type='TIMESTAMP', default=PydanticUndefined)                                                                                                                      
                                                                                                  |        | t6_1 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t6_1', type_=ModelField(name='t6_1', type=str, required=False, default='test'))]) , ExpectedResult(is_optional=False, sql_type='TEXT', default='test')                                                                                                                          
                                                                                                  |        | t6_2 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t6_2', type_=ModelField(name='t6_2', type=Optional[str], required=False, default=None))]) , ExpectedResult(is_optional=True, sql_type='TEXT', default=None)                                                                                                                     
                                                                                                  |        | t6_3 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t6_3', type_=ModelField(name='t6_3', type=int, required=False, default=69))]) , ExpectedResult(is_optional=False, sql_type='BIGINT', default=69)                                                                                                                                
                                                                                                  |        | t6_4 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t6_4', type_=ModelField(name='t6_4', type=str, required=False, default='this test will proof if "something" ain\'t escaped properly. ^^\''))]) , ExpectedResult(is_optional=False, sql_type='TEXT', default='this test will proof if "something" ain\'t escaped properly. ^^\'')
                                                                                                  |        | t7_1 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t7_1', type_=ModelField(name='t7_1', type=OtherTable, required=True))]) , ExpectedResult(is_optional=False, sql_type='JSONB', default=PydanticUndefined)                                                                                                                        
                                                                                                  |        | t8_1 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t8_1', type_=ModelField(name='t8_1', type=list, required=True))]) , ExpectedResult(is_optional=False, sql_type='JSONB', default=PydanticUndefined)                                                                                                                              
                                                                                                  |        | t8_2 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t8_2', type_=ModelField(name='t8_2', type=List[int], required=True))]) , ExpectedResult(is_optional=False, sql_type='BIGINT[]', default=PydanticUndefined)                                                                                                                      
                                                                                                  |        | t8_3 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t8_3', type_=ModelField(name='t8_3', type=List[List], required=True))]) , ExpectedResult(is_optional=False, sql_type='BIGINT[][]', default=PydanticUndefined)                                                                                                                   
                                                                                                  |        | t8_4 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t8_4', type_=ModelField(name='t8_4', type=List[List], required=True))]) , ExpectedResult(is_optional=False, sql_type='JSONB', default=PydanticUndefined)                                                                                                                        
                                                                                                  |        | t9_1 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t9_1', type_=ModelField(name='t9_1', type=Tuple[int, int, int], required=True))]) , ExpectedResult(is_optional=False, sql_type='BIGINT[]', default=PydanticUndefined)                                                                                                           
                                                                                                  |        | t9_2 , FieldTypehint(is_primary_key=False, types=[FieldItem(field='t9_2', type_=ModelField(name='t9_2', type=Tuple[int, str, float], required=True))]) , ExpectedResult(is_optional=False, sql_type='JSONB', default=PydanticUndefined)                                                                                                            
test_type_detection_typing                                                                        | ✅ pass             | t0_id , <class 'int'> , ExpectedResult(is_optional=False, sql_type='BIGINT', default=PydanticUndefined)                                                                                                                                                                                                                                            
                                                                                                  |        | t1_1 , <class 'str'> , ExpectedResult(is_optional=False, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                                                                                                                               
                                                                                                  |        | t1_2 , <class 'str'> , ExpectedResult(is_optional=False, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                                                                                                                               
                                                                                                  |        | t1_3 , <class 'str'> , ExpectedResult(is_optional=False, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                                                                                                                               
                                                                                                  |        | t1_4 , <class 'str'> , ExpectedResult(is_optional=False, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                                                                                                                               
                                                                                                  |        | t2_1 , typing.Optional[str] , ExpectedResult(is_optional=True, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                                                                                                                         
                                                                                                  |        | t2_4 , typing.Optional[str] , ExpectedResult(is_optional=True, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                                                                                                                         
                                                                                                  |        | t2_5 , typing.Optional[str] , ExpectedResult(is_optional=True, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                                                                                                                         
                                                                                                  |        | t2_6 , typing.Optional[str] , ExpectedResult(is_optional=True, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                                                                                                                         
                                                                                                  |        | t3_1 , <class 'str'> , ExpectedResult(is_optional=False, sql_type='TEXT', default=PydanticUndefined)                                                                                                                                                                                                                                               
                                                                                                  |        | t3_2 , <class 'int'> , ExpectedResult(is_optional=False, sql_type='BIGINT', default=PydanticUndefined)                                                                                                                                                                                                                                             
                                                                                                  |        | t3_3 , <class 'float'> , ExpectedResult(is_optional=False, sql_type='DOUBLE PRECISION', default=PydanticUndefined)                                                                                                                                                                                                                                 
                                                                                                  |        | t3_4 , <class 'bool'> , ExpectedResult(is_optional=False, sql_type='BOOLEAN', default=PydanticUndefined)                                                                                                                                                                                                                                           
                                                                                                  |        | t5_1 , <class 'datetime.datetime'> , ExpectedResult(is_optional=False, sql_type='TIMESTAMP', default=PydanticUndefined)                                                                                                                                                                                                                            
                                                                                                  |        | t6_1 , <class 'str'> , ExpectedResult(is_optional=False, sql_type='TEXT', default='test')                                                                                                                                                                                                                                                          
                                                                                                  |        | t6_2 , typing.Optional[str] , ExpectedResult(is_optional=True, sql_type='TEXT', default=None)                                                                                                                                                                                                                                                      
                                                                                                  |        | t6_3 , <class 'int'> , ExpectedResult(is_optional=False, sql_type='BIGINT', default=69)                                                                                                                                                                                                                                                            
                                                                                                  |        | t6_4 , <class 'str'> , ExpectedResult(is_optional=False, sql_type='TEXT', default='this test will proof if "something" ain\'t escaped properly. ^^\'')                                                                                                                                                                                             
                                                                                                  |        | t7_1 , <class 'test_create_table.OtherTable'> , ExpectedResult(is_optional=False, sql_type='JSONB', default=PydanticUndefined)                                                                                                                                                                                                                     
                                                                                                  |        | t8_1 , <class 'list'> , ExpectedResult(is_optional=False, sql_type='JSONB', default=PydanticUndefined)                                                                                                                                                                                                                                             
                                                                                                  |        | t8_2 , typing.List[int] , ExpectedResult(is_optional=False, sql_type='BIGINT[]', default=PydanticUndefined)                                                                                                                                                                                                                                        
                                                                                                  |        | t8_3 , typing.List[typing.List[int]] , ExpectedResult(is_optional=False, sql_type='BIGINT[][]', default=PydanticUndefined)                                                                                                                                                                                                                         
                                                                                                  |        | t8_4 , typing.List[typing.List[typing.Union[str, int]]] , ExpectedResult(is_optional=False, sql_type='JSONB', default=PydanticUndefined)                                                                                                                                                                                                           
                                                                                                  |        | t9_1 , typing.Tuple[int, int, int] , ExpectedResult(is_optional=False, sql_type='BIGINT[]', default=PydanticUndefined)                                                                                                                                                                                                                             
                                                                                                  |        | t9_2 , typing.Tuple[int, str, float] , ExpectedResult(is_optional=False, sql_type='JSONB', default=PydanticUndefined)                                                                                                                                                                                                                              


### `test_create_table_online.CreateTableOnlineTestCase` <a name="test_create_table_online.CreateTableOnlineTestCase" />

              Test name                | Status | Stack
-------------------------------------- | ------ | -----
test_sql_text_connection_missing       | ✅ pass             |      
test_sql_text_connection_typeerror     | ✅ pass             |      
test_sql_text_connection_valid_asyncpg | ✅ pass             |      
test_sql_text_connection_valid_psycop2 | ✅ pass             |      


### `test_delete_row.UpdateRowTestCase` <a name="test_delete_row.UpdateRowTestCase" />

Test name | Status | Stack
--------- | ------ | -----
test_foo  | ✅ pass             |      


### `doctest.DocTestCase` <a name="doctest.DocTestCase" />

                              Test name                               | Status | Stack
--------------------------------------------------------------------- | ------ | -----
get_fields_references: Doctest: fastorm.FastORM.get_fields_references | ✅ pass             |      
get_fields_typehints: Doctest: fastorm.FastORM.get_fields_typehints   | ✅ pass             |      
get_table: Doctest: fastorm.FastORM.get_table                         | ✅ pass             |      
match_type: Doctest: fastorm.FastORM.match_type                       | ✅ pass             |      


### `test_get_fields.MyTestCase` <a name="test_get_fields.MyTestCase" />

    Test name     | Status |                                                                                                                                                                                                                                                                              Stack                                                                                                                                                                                                                                                                              
----------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_flattened    | ✅ pass             | {'cool_reference__id_part_1': FieldTypehint(is_primary_key=True, types=[FieldItem(field='cool_reference', type_=ModelField(name='cool_reference', type=OtherTable, required=True)), FieldItem(field='id_part_1', type_=ModelField(name='id_part_1', type=int, required=True))]), 'cool_reference__id_part_2': FieldTypehint(is_primary_key=True, types=[FieldItem(field='cool_reference', type_=ModelField(name='cool_reference', type=OtherTable, required=True)), FieldItem(field='id_part_2', type_=ModelField(name='id_part_2', type=str, required=True))])}
test_not_fattened | ✅ pass             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 


### `test_get_fields_references.GetFieldsReferencesMultiLayerReferenceTest` <a name="test_get_fields_references.GetFieldsReferencesMultiLayerReferenceTest" />

             Test name               | Status | Stack
------------------------------------ | ------ | -----
test_two_level_on_double_reference_1 | ✅ pass             |      
test_two_level_on_double_reference_2 | ✅ pass             |      


### `test_get_fields_references.GetFieldsReferencesSimpleTest` <a name="test_get_fields_references.GetFieldsReferencesSimpleTest" />

             Test name              | Status | Stack
----------------------------------- | ------ | -----
test_simple_double_key_no_recursive | ✅ pass             |      
test_simple_double_key_recursive    | ✅ pass             |      
test_simple_single_key_no_recursive | ✅ pass             |      
test_simple_single_key_recursive    | ✅ pass             |      


### `test_get_fields_references.GetFieldsReferencesSingleReferenceTest` <a name="test_get_fields_references.GetFieldsReferencesSingleReferenceTest" />

                     Test name                      | Status | Stack
--------------------------------------------------- | ------ | -----
test_single_reference_double_key_no_recursive       | ✅ pass             |      
test_single_reference_no_pk_double_key_recursive    | ✅ pass             |      
test_single_reference_no_pk_single_key_no_recursive | ✅ pass             |      
test_single_reference_no_pk_single_key_recursive    | ✅ pass             |      
test_single_reference_single_key_recursive          | ✅ pass             |      
test_single_reference_stacked_pk_key_no_recursive   | ✅ pass             |      


### `test_get_fields_typehints.GetFieldsReferencesSimpleTest` <a name="test_get_fields_typehints.GetFieldsReferencesSimpleTest" />

             Test name              | Status | Stack
----------------------------------- | ------ | -----
test_simple_double_key_no_recursive | ✅ pass             |      


### `test_insert_row.InsertRowTestCase` <a name="test_insert_row.InsertRowTestCase" />

 Test name  | Status | Stack
----------- | ------ | -----
test_insert | ✅ pass             |      


### `test_select_row.SelectRowTestCase` <a name="test_select_row.SelectRowTestCase" />

 Test name   | Status | Stack
------------ | ------ | -----
test_foo     | ✅ pass             |      
test_foo_bar | ✅ pass             |      


### `test_table_metadata.TableMetadataTestCase` <a name="test_table_metadata.TableMetadataTestCase" />

      Test name        | Status | Stack
---------------------- | ------ | -----
test_automatic_fields  | ✅ pass             |      
test_ignored_fields    | ✅ pass             |      
test_primary_keys      | ✅ pass             |      
test_table_name        | ✅ pass             |      
test_table_quoted_name | ✅ pass             |      


### `test_table_references.CreateTableTestCase` <a name="test_table_references.CreateTableTestCase" />

                  Test name                    | Status | Stack
---------------------------------------------- | ------ | -----
test_working_table_multi_references_mandatory  | ✅ pass             |      
test_working_table_multi_references_optional   | ✅ pass             |      
test_working_table_single_references_mandatory | ✅ pass             |      
test_working_table_single_references_optional  | ✅ pass             |      


### `test_update_row.UpdateRowTestCase` <a name="test_update_row.UpdateRowTestCase" />

Test name | Status | Stack
--------- | ------ | -----
test_foo  | ✅ pass             |      
