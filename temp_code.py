

import code_timer

def key_function( item ):
        #return item * item
        return item

loop_max   = 10000

a_code_timer = code_timer.CodeTimer()

a_code_timer.start( "Just sort" )

for i in range( loop_max ):
    somelist = [1, -3, 6, 11, 5]
    somelist.sort()

a_code_timer.stop(   )
# ---- "Sort with key function "
a_code_timer.start( "Sort with key function " )

for i in range( loop_max ):
    somelist = [1, -3, 6, 11, 5]
    somelist.sort( key = key_function )
print( somelist )
a_code_timer.stop(   )
print( somelist )

a_code_timer.start( "Sort with key lambda function " )

for i in range( loop_max ):
    somelist = [1, -3, 6, 11, 5]
    somelist.sort( key = lambda item : ( item )   )
print( somelist )
a_code_timer.stop(   )
print( somelist )
a_code_timer.report(   )

print( '\n\n' )
# Python program to illustrate
# using keys for sorting
somelist = [1, -3, 6, 11, 5]
somelist.sort()
print( somelist )

s = 'geeks'
# use sorted() if you don't want to sort in-place:
s = sorted(s)
print( s )














1/0


import code_timer

loop_max   = 100
a_code_timer = code_timer.CodeTimer()

for i in range( loop_max ):
    squ   = i*i

# ---- no try
a_code_timer.start( "Warmup Without Try" )

for i in range( loop_max ):
    squ   = i*i

a_code_timer.stop(   )

# ----  try
a_code_timer.start( "With Try" )

try:
    for i in range( loop_max ):
        squ   = i*i

except Exception as an_exception:
    print( an_exception )

a_code_timer.stop(   )


# ---- no try
a_code_timer.start( "Reference without Try" )

for i in range( loop_max ):
    squ   = i*i

a_code_timer.stop(   )

# ----
a_code_timer.report(   )






