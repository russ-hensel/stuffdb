


class ExClass():
    def __init__( self ):
        pass

    def replacable_method( self ):
        print( "replacable method not replaced")

    def a_method( self ):
        print( "a_method" )

    def b_method( self ):
        print( "b_method" )

print( "\nUse direct call to the functin")
ex_class    = ExClass()

ex_class.replacable_method()
ex_class.replacable_method    = ex_class.a_method
ex_class.replacable_method()

ex_class.a_method  = ex_class.b_method
ex_class.replacable_method()


print( "\nDo it again with lambda() which seems to give later binding")
ex_class    = ExClass()

ex_class.replacable_method()
ex_class.replacable_method    = lambda:ex_class.a_method()
ex_class.replacable_method()

ex_class.a_method  = ex_class.b_method
ex_class.replacable_method()

print( "\nDo it again with lambda no () which does not work at all ")
ex_class    = ExClass()

ex_class.replacable_method()
ex_class.replacable_method    = lambda:ex_class.a_method
ex_class.replacable_method()

ex_class.a_method  = ex_class.b_method
ex_class.replacable_method()



