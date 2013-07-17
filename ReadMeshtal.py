#############################
#
#    Basic Meshtally Reader
#
#############################

import sys
import linecache

#############################

def locate( string, char ):
    for i in range(len(string)):
        if string[i] == char:
            return i
    return -1
    
def find_in_iterable(x, iterable):
    for i, item in enumerate(iterable):
        if item == x:
            return i
    return -1
    
def hit( FileName, Lines, LineCount ):
    for i in range(Lines):
        if (linecache.getline(FileName,LineCount+i).split() != []):
            return True
    return False

#############################

def ReadMeshtalHead( FileName, LineCount ):

    #
    # Action:
    #     Extract header data
    # Input:
    #     FileName: path of meshtal file
    #     LineCount: Line from which parsing should start
    # Output:
    #     Header: array containing mcnp version and no. of histories
    #     LineCount: Last line used for parsing
    #
 
    # Header = ['mcnp version', 'no. of histories']
    Header = ['-1', '-1']
    Flag = len(Header) 
    m = LineCount
    
    while Flag:
        Line = linecache.getline( FileName, LineCount )
        LineCount = LineCount+1
        
        # empty line
        if ( Line.split() == []):
            continue
        
        # ignore comments
        x = locate( Line.strip(), '#' )
        if ( x == 0 ):
            continue
        elif (x > 0):
            Line = str(Line.split('#')[:1]).lower().split()
        else:
            Line = Line.lower().split()
        
        # get mcnp version
        if ( Header[0] == '-1' ) & ( 'mcnp' in Line ) & ( 'version' in Line ):
            for i in range(Line.index('version')+1,len(Line)):            
                if Line[i].replace('.','').isdigit():
                    Header[0] = Line[i]
                    Flag = Flag-1
                    break
            
        # get number of histories
        elif ( Header[1] == '-1' ) & ( 'number' in Line ) & ( 'histories' in Line ):
            for i in Line:
                if i.replace('.','').isdigit():
                    Header[1] = i
                    Flag = Flag-1
                    break
         
        elif (LineCount - m) > 50:
            break

    return Header, (LineCount)
                
#############################

def ReadMeshtallyHead( FileName, LineCount ):

    #
    # Action:
    #     Extract Meshtally number and type
    # Input:
    #     FileName: path of meshtal file
    #     LineCount: Line from which parsing should start
    # Output:
    #     Header: array containing meshtally number and meshtally type
    #     LineCount: Last line used for parsing
    #

    # header = ['meshtally no.', 'meshtally type']
    Header = ['-1', '-1']
    flag = 2  
    m = LineCount
    
    while flag:
        Line = linecache.getline( FileName, LineCount )
        LineCount = LineCount+1
        
        # empty line
        if ( Line.split() == []):
            continue
        
        # ignore comments
        x = locate( Line.strip(), '#' )
        if ( x == 0 ):
            continue
        elif (x > 0):
            Line = str(Line.split('#')[:1]).lower().split()
        else:
            Line = Line.lower().split()
 
        # get meshtally number
        if ( Header[0] == '-1') & ('mesh' in Line) & ('tally' in Line) & ('number' in Line):
            for i in Line:
                if i.replace('.','',1).isdigit():
                    Header[0] = i
                    flag = flag-1
                    break
    
        # get meshtally type
        elif ( Header[1] == '-1' ) & ('is' in Line) & ('mesh' in Line) & (('tally.' in Line) | ('tally' in Line)):
            if ('and' in Line ) & ('neutron' in Line ) & ('photon' in Line ):
                Header[1] = 'np'
                flag = flag-1
            elif ('neutron' in Line):
                Header[1] = 'n'
                flag = flag-1
            elif ('photon' in Line):
                Header[1] = 'p'
                flag = flag-1
        
        elif (LineCount - m) > 50:
            break

    return Header, (LineCount)          
                
#############################
    
def ReadBoundaries( FileName, LineCount ):

    #
    # Action:
    #     Extract x,y,z and energy bin bounds
    # Input:
    #     FileName: path of meshtal file
    #     LineCount: Line from which parsing should start
    # Output:
    #     x_direction: array of x_direction boundary points
    #     y_direction: array of y_direction boundary points
    #     z_direction: array of z_direction boundary points
    #     e_bounds: array of energy bounds
    #     LineCount: Last line used for parsing
    #

    x_direction = []
    y_direction = []
    z_direction = []
    e_bounds = []

    flag = 4  
    m = LineCount
    
    while flag:
        Line = linecache.getline( FileName, LineCount )
        LineCount = LineCount+1
        
        # empty line
        if ( Line.split() == []):
            continue
        
        # ignore comments
        x = locate( Line.strip(), '#' )
        if ( x == 0 ):
            continue
        elif (x > 0):
            Line = str(Line.split('#')[:1]).lower().replace(':','').split()
        else:
            Line = Line.lower().replace(':','').split()

        # get x bounds
        if (x_direction == []) & ('x' in Line) & ('direction' in Line):
            for i in Line:
                if i.replace('-','').replace('.','').isdigit():
                    x_direction.append(i)
            flag = flag-1
                    
        # get y bounds
        elif (y_direction == []) & ('y' in Line) & ('direction' in Line):
            for i in Line:
                if i.replace('-','').replace('.','').isdigit():
                    y_direction.append(i)
            flag = flag-1
                    
        # get z bounds
        elif (z_direction == []) & ('z' in Line) & ('direction' in Line):
            for i in Line:
                if i.replace('-','').replace('.','').isdigit():
                    z_direction.append(i)
            flag = flag-1

        # get energy bounds
        elif (e_bounds == []) & ('energy' in Line) & ('bin' in Line):
            for i in Line:
                if i.replace('+','').replace('-','').replace('.','').replace('e','').isdigit():
                    e_bounds.append(i.replace('e','E')) 
            flag = flag-1               

        elif (LineCount - m) > 50:
            break
            
    return x_direction, y_direction, z_direction, e_bounds, (LineCount)
    
#############################

def ReadFirstLine( FileName, LineCount ):

    #
    # Action:
    #     Extract order in which result and error values are listed
    # Input:
    #     FileName: path of meshtal file
    #     LineCount: Line from which parsing should start
    # Output:
    #     a: array containing order of listing of results
    #     LineCount: Last line used for parsing
    #

    #   a = ['x','y','z','result','rel_error','energy','volume','res*vol']
    a = [-1,-1,-1,-1,-1,-1,-1,-1]
    
    flag = 1  
    m = LineCount
    
    while flag:
        Line = temp = linecache.getline( FileName, LineCount )
        LineCount = LineCount+1
        
        # empty line
        if ( Line.split() == []):
            continue
        
        # ignore comments
        x = locate( Line.strip(), '#' )
        if ( x == 0 ):
            continue
        elif (x > 0):
            Line = str(Line.split('#')[:1]).lower().replace(':','').split()
        else:
            Line = Line.lower().replace(':','').split()

        if ('x' in Line) & ('y' in Line) & ('z' in Line) & ('result' in Line):
            temp = temp.lower().replace('rel ','rel').replace('rslt * ','rslt').strip().split()
            
            a[0] = find_in_iterable('x',temp)
            a[1] = find_in_iterable('y',temp)
            a[2] = find_in_iterable('z',temp)
            a[3] = find_in_iterable('result',temp)
            a[4] = find_in_iterable('relerror',temp)
            a[5] = find_in_iterable('energy',temp)
            a[6] = find_in_iterable('volume',temp)
            a[7] = find_in_iterable('rsltvol',temp)
            
            flag = flag-1

    return a, (LineCount)
    
#############################

def ReadValues( FileName, LineCount, a ):

    #
    # Action:
    #     Extract meshtally values
    # Input:
    #     FileName: path of meshtal file
    #     LineCount: Line from which parsing should start
    #     a: array containing order of listing of results
    # Output:
    #     x_val, y_val, z_val, n_val: arrays containing x, y, z and energy values
    #     r_val, e_val: arrays containing result and relerror values
    #     LineCount: Last line used for parsing
    #

    x_val = []
    y_val = []
    z_val = []
    n_val = []
    r_val = []
    e_val = []    
    
    flag = 1  
    m = LineCount
    
    while flag:
    
        Line = linecache.getline(FileName, LineCount)
                        
        if hit(FileName, 1, LineCount) == False:
            flag = flag-1
            break

        else:
            LineCount += 1
            Line = Line.split()
                    	
            try:
                x_val.append(Line[a[0]])         # x_val
            except IndexError:
                print 'x_val not found'
                            
            try:
                y_val.append(Line[a[1]])         # y_val
            except IndexError:
                print 'y_val not found'
                            
            try:
                z_val.append(Line[a[2]])         # z_val
            except IndexError:
                print 'z_val not found'
                        
            try:
                r_val.append(Line[a[3]])         # result
            except IndexError:
                print 'r_val not found'

            try:
                n_val.append(Line[a[5]])         # energy
            except IndexError:
                print 'e_val not found'

            try:
                e_val.append(Line[a[4]])         # relerror
            except IndexError:
                print 'e_val not found'

    return x_val, y_val, z_val, n_val, r_val, e_val, (LineCount)
    
#############################

def ReadMeshtal( FileName ):

    #    1. get number of histories for normalizing tallies
    #    2. for each meshtally, get type and number
    #    3. find x,y,z bounds and energy bin boundaries
    #    4. read and return x,y,z values with energy and result
    #

    #
    # Action:
    #     Reads an MCNP meshtal file
    # Input:
    #     FileName: path of meshtal file
    # Output:
    #     Meshtal file header
    #     Any number of meshtallies
    #

    mcnp_version = -1
    histories = -1.0
    MeshtallyCount = 0
    MeshtallyLine = []

    meshtally_number = []
    meshtally_type = []

    x_direction = []
    y_direction = []
    z_direction = []
    e_bounds = []
    
    x_val = []    #    store x bounds
    y_val = []    #    store y bounds
    z_val = []    #    store z bounds
    r_val = []    #    store result values
    e_val = []    #    store relerror values
    n_val = []    #    store energy values
    v_val = []    #    store volume
    f_val = []    #    store result * volume

    a = [-1,-1,-1,-1,-1,-1,-1,-1]
    #   a = ['x','y','z','result','rel_error','energy','volume','res*vol']

    LineCount = 0
    Temp = []
    LineTemp = 0  
    
    Temp, LineTemp = ReadMeshtalHead( FileName, LineCount+1 )
        
    if LineTemp == LineCount:
    	  print "LineCount error! Empty file? #01"
    else: 
        MeshtallyLine.append(LineCount)
        LineCount = LineTemp
        if Temp[0] == '-1':
            print "Can't read mcnp version"
        else:
            mcnp_version = Temp[0]
    
        if Temp[1] == '-1':
            print "Can't read no. of histories"
        else:
            histories = Temp[1]

    while hit( FileName, 20, LineCount ):
        Temp, LineTemp = ReadMeshtallyHead( FileName, LineCount+1 )
                	       
        if LineTemp == LineCount:
            print "LineCount error! End of file? #02"
        else: 
            MeshtallyLine.append(LineCount)
            LineCount = LineTemp       
            MeshtallyCount = MeshtallyCount + 1
        
            if Temp[0] == '-1':
                print "Can't read meshtally number"
            else:
            	  meshtally_number.append(Temp[0])
    
            if Temp[1] == '-1':
            	  print "Can't read meshtally type"
            else:
            	  meshtally_type.append(Temp[1])
        	  
        x_direction, y_direction, z_direction, e_bounds, LineTemp = ReadBoundaries( FileName, LineCount+1 )
    
        if LineTemp == LineCount:
        	  print "LineCount error! End of file? #03"
        else: 
            MeshtallyLine.append(LineCount)
            LineCount = LineTemp
        
            if x_direction == []:
                print "Can't read x_direction"
            if y_direction == []:
                print "Can't read y_direction"
            if z_direction == []:
                print "Can't read z_direction"
            if e_bounds == []:
                print "Can't read e_bounds"
            
        a, LineTemp = ReadFirstLine( FileName, LineCount+1 )
    
        if LineTemp == LineCount:
        	  print "LineCount error! End of file? #04"
        else: 
            MeshtallyLine.append(LineCount)
            LineCount = LineTemp
        
            if a == []:
                print "can't read a"

        x_val, y_val, z_val, n_val, r_val, e_val, LineTemp = ReadValues( FileName, LineCount+1, a )
        MeshtallyLine.append(LineCount)
        LineCount = LineTemp       
        
        print '\nmeshtally number: ', meshtally_number[-1]
        print 'meshtally type: ', meshtally_type[-1]

        print '\nTally bin boundaries:'
        print 'x_direction:', x_direction
        print 'y_direction:', y_direction
        print 'z_direction:', z_direction

        print '\ne_bounds:', e_bounds

        print '\nn_val       x_val       y_val       z_val       r_val       e_val' 
            
        for i in range(len(n_val)):
            print n_val[i], '  ', x_val[i], '  ', y_val[i], '  ', z_val[i], '  ', r_val[i], '  ', e_val[i]
            
#        if MeshtallyCount == 5:
#            break

    print '\nmcnp_version: ', mcnp_version
    print 'Number of histories: ', histories
    print 'Number of meshtallies found: ', MeshtallyCount      
        	   
    return True
    
#############################   
#############################
  
ReadMeshtal( 'text.txt' )
            
#############################  
