def bus_name_lists():
    """Get lists with bus names and phases
    First list is for 1p buses, with bus name and phase number
    Second list is for 2p buses, with bus name, bus1, bus2 and phase numbers
    Third list is for 3p buses, with bus name
    These are the buses that will go into the simulation
    """
    import re

    bus_list_1p = []
    bus_list_2p = []
    bus_list_3p = []

    with open("ckt24\\lines_ckt24.dss","r") as lines_file:
        lines_data = lines_file.readlines()

    for i in range(len(lines_data)):
        # Check if line is a commentary
        if lines_data[i][0] is not "!":
            line_list = lines_data[i].split()

            # Loop that appends bus1 to list
            for j in range(len(line_list)):

                bus1_insensitive = re.sub("bus1","BUS1",line_list[j],
                                          flags=re.IGNORECASE)
                if "BUS1" in bus1_insensitive:
                    bus1 = bus1_insensitive.replace("BUS1=","")

                    if ".1.2.3" in bus1_insensitive:
                        nphases = "3"

                    elif any(x in bus1_insensitive for x in [".1.2",".2.1"]):
                        phase = [1,2]
                        nphases = "2"
                    elif any(x in bus1_insensitive for x in [".1.3",".3.1"]):
                        phase = [1,3]
                        nphases = "2"
                    elif any(x in bus1_insensitive for x in [".2.3",".3.2"]):
                        phase = [2,3]
                        nphases = "2"

                    elif ".1" in bus1_insensitive:
                        phase = 1
                        nphases = "1"
                    elif ".2" in bus1_insensitive:
                        phase = 2
                        nphases = "1"
                    elif ".3" in bus1_insensitive:
                        phase = 3
                        nphases = "1"

            if nphases == "1":
                bus_list_1p.append([bus1, phase])

            if nphases == "2":
                bus_list_2p.append([bus1, phase[0], phase[1]])

            if nphases == "3":
                bus_list_3p.append([bus1])


            # Loop that appends bus2 to list
            for j in range(len(line_list)):

                bus2_insensitive = re.sub("bus2","BUS2",line_list[j],
                                          flags=re.IGNORECASE)
                if "BUS2" in bus2_insensitive:
                    bus2 = bus2_insensitive.replace("BUS2=","")

                    if ".1.2.3" in bus2_insensitive:
                        nphases = "3"

                    elif any(x in bus2_insensitive for x in [".1.2",".2.1"]):
                        phase = [1,2]
                        nphases = "2"
                    elif any(x in bus2_insensitive for x in [".1.3",".3.1"]):
                        phase = [1,3]
                        nphases = "2"
                    elif any(x in bus2_insensitive for x in [".2.3",".3.2"]):
                        phase = [2,3]
                        nphases = "2"

                    elif ".1" in bus2_insensitive:
                        phase = 1
                        nphases = "1"
                    elif ".2" in bus2_insensitive:
                        phase = 2
                        nphases = "1"
                    elif ".3" in bus2_insensitive:
                        phase = 3
                        nphases = "1"

            if nphases == "1":
                bus_list_1p.append([bus2, phase])

            if nphases == "2":
                bus_list_2p.append([bus2, phase[0], phase[1]])

            if nphases == "3":
                bus_list_3p.append([bus2])

    # Exclude repeated buses
    bus_list_1p = sorted(bus_list_1p)
    bus_list_1p = [bus_list_1p[i] for i in range(len(bus_list_1p)) if i == 0 \
    or bus_list_1p[i][0].split('.')[0] != bus_list_1p[i-1][0].split('.')[0]]

    bus_list_2p = sorted(bus_list_2p)
    bus_list_2p = [bus_list_2p[i] for i in range(len(bus_list_2p)) if i == 0 \
    or bus_list_2p[i][0].split('.')[0] != bus_list_2p[i-1][0].split('.')[0]]

    bus_list_3p = sorted(bus_list_3p)
    bus_list_3p = [bus_list_3p[i] for i in range(len(bus_list_3p)) if i == 0 \
    or bus_list_3p[i][0].split('.')[0] != bus_list_3p[i-1][0].split('.')[0]]

    for i in range(len(bus_list_1p)):
        for j in range(len(bus_list_3p)):
            if bus_list_3p[j][0].split('.')[0] == \
            bus_list_1p[i][0].split('.')[0]:
                bus_list_1p[i] = "remove"
        for j in range(len(bus_list_2p)):
            if bus_list_2p[j][0].split('.')[0] == \
            bus_list_1p[i][0].split('.')[0]:
                bus_list_1p[i] = "remove"
    bus_list_1p = [x for x in bus_list_1p if x != "remove"]

    for i in range(len(bus_list_2p)):
        for j in range(len(bus_list_3p)):
            if bus_list_3p[j][0].split('.')[0] == \
            bus_list_2p[i][0].split('.')[0]:
                bus_list_2p[i] = "remove"
    bus_list_2p = [x for x in bus_list_2p if x != "remove"]

    # Reads "bus.1.2.3" as "bus"
    for i in range(len(bus_list_1p)):
        bus_list_1p[i][0] = bus_list_1p[i][0].split('.')[0]
    for i in range(len(bus_list_2p)):
        bus_list_2p[i][0] = bus_list_2p[i][0].split('.')[0]
    for i in range(len(bus_list_3p)):
        bus_list_3p[i][0] = bus_list_3p[i][0].split('.')[0]

    # Add geographical coordinates to bus
    with open("ckt24\\buscoords_ckt24.dss","r") as coordinates_file:
        bus_coords = coordinates_file.readlines()

    for i in range(len(bus_coords)):
        for j in range(len(bus_list_1p)):
            if bus_coords[i].split()[0] == bus_list_1p[j][0]:
                bus_list_1p[j].insert(1,bus_coords[i].split()[1])
                bus_list_1p[j].insert(2,bus_coords[i].split()[2])


        for j in range(len(bus_list_2p)):
            if bus_coords[i].split()[0] == bus_list_2p[j][0]:
                bus_list_2p[j].insert(1,bus_coords[i].split()[1])
                bus_list_2p[j].insert(2,bus_coords[i].split()[2])

        for j in range(len(bus_list_3p)):
            if bus_coords[i].split()[0] == bus_list_3p[j][0]:
                bus_list_3p[j].append(bus_coords[i].split()[1])
                bus_list_3p[j].append(bus_coords[i].split()[2])

    # Remove buses without coordinates
    remove_list = []
    for i in range(len(bus_list_1p)):
        if len(bus_list_1p[i]) != 4:
            remove_list.append(i)
    for index in remove_list:
        bus_list_1p.remove(bus_list_1p[index])

    remove_list = []
    for i in range(len(bus_list_2p)):
        if len(bus_list_2p[i]) != 5:
            remove_list.append(i)
    for index in remove_list:
        bus_list_1p.remove(bus_list_2p[index])

    remove_list = []
    for i in range(len(bus_list_3p)):
        if len(bus_list_3p[i]) != 3:
            remove_list.append(i)
    for index in remove_list:
        bus_list_1p.remove(bus_list_3p[index])

    return [bus_list_1p, bus_list_2p, bus_list_3p]

def line_name_lists():
    """Get lists with line names and phases
    First list is for 1p lines, with line name, bus1, bus2
    Second list is for 2p lines, with line name, bus1, bus2
    Third list is for 3p with line name, bus1, bus2
    These are the lines that will go into the plot
    """

    import re
    import os

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

    line_list_1p = []
    line_list_2p = []
    line_list_3p = []

    with open("ckt24\\lines_ckt24.dss","r") as lines_file:
        lines_data = lines_file.readlines()

    for i in range(len(lines_data)):
        # Check if line is a commentary
        if lines_data[i][0] is not "!":
            line_list = lines_data[i].split()

            for j in range(len(line_list)):

                # Line name
                line_name_insensitive = re.sub("line[.]","LINE.",line_list[j],
                                               flags=re.IGNORECASE)
                if "LINE." in line_name_insensitive :
                    line_name = line_name_insensitive.replace("LINE.","")

                # Number of phases of line
                nphases_insensitive = re.sub("phases","PHASES",line_list[j],
                                             flags=re.IGNORECASE)
                if "PHASES" in nphases_insensitive:
                    nphases = nphases_insensitive.replace("PHASES=","")

                # Bus1 and phases of line
                bus1_insensitive = re.sub("bus1","BUS1",line_list[j],
                                          flags=re.IGNORECASE)
                if "BUS1" in bus1_insensitive:
                    bus1 = bus1_insensitive.replace("BUS1=","")

                    if ".1.2.3" in bus1_insensitive:
                        pass

                    elif any(x in bus1_insensitive for x in [".1.2",".2.1"]):
                        phase = [1,2]
                    elif any(x in bus1_insensitive for x in [".1.3",".3.1"]):
                        phase = [1,3]
                    elif any(x in bus1_insensitive for x in [".2.3",".3.2"]):
                        phase = [2,3]

                    elif ".1" in bus1_insensitive:
                        phase = 1
                    elif ".2" in bus1_insensitive:
                        phase = 2
                    elif ".3" in bus1_insensitive:
                        phase = 3

                # Bus2 of line
                bus2_insensitive = re.sub("bus2","BUS2",line_list[j],
                                          flags=re.IGNORECASE)
                if "BUS2" in bus2_insensitive:
                    bus2 = bus2_insensitive.replace("BUS2=","")

            if nphases == "1":
                line_list_1p.append([line_name,bus1,bus2,phase])

            elif nphases == "2":
                line_list_2p.append([line_name,bus1,bus2,phase])

            else:
                line_list_3p.append([line_name,bus1,bus2])

    # Reads "bus.1.2.3" as "bus"
    for i in range(len(line_list_1p)):
        line_list_1p[i][1] = line_list_1p[i][1].split('.')[0]
        line_list_1p[i][2] = line_list_1p[i][2].split('.')[0]

    for i in range(len(line_list_2p)):
        line_list_2p[i][1] = line_list_2p[i][1].split('.')[0]
        line_list_2p[i][2] = line_list_2p[i][2].split('.')[0]

    for i in range(len(line_list_3p)):
        line_list_3p[i][1] = line_list_3p[i][1].split('.')[0]
        line_list_3p[i][2] = line_list_3p[i][2].split('.')[0]

    # Add geographical coordinates to bus
    with open("ckt24\\buscoords_ckt24.dss","r") as coordinates_file:
        bus_coords = coordinates_file.readlines()

    for i in range(len(bus_coords)):
        for j in range(len(line_list_1p)):
            if bus_coords[i].split()[0] == line_list_1p[j][1]:
                line_list_1p[j].append(bus_coords[i].split()[1])
                line_list_1p[j].append(bus_coords[i].split()[2])
    for i in range(len(bus_coords)):
        for j in range(len(line_list_1p)):
            if bus_coords[i].split()[0] == line_list_1p[j][2]:
                line_list_1p[j].append(bus_coords[i].split()[1])
                line_list_1p[j].append(bus_coords[i].split()[2])

    for i in range(len(bus_coords)):
        for j in range(len(line_list_2p)):
            if bus_coords[i].split()[0] == line_list_2p[j][1]:
                line_list_2p[j].append(bus_coords[i].split()[1])
                line_list_2p[j].append(bus_coords[i].split()[2])
    for i in range(len(bus_coords)):
        for j in range(len(line_list_2p)):
            if bus_coords[i].split()[0] == line_list_2p[j][2]:
                line_list_2p[j].append(bus_coords[i].split()[1])
                line_list_2p[j].append(bus_coords[i].split()[2])

    for i in range(len(bus_coords)):
        for j in range(len(line_list_3p)):
            if bus_coords[i].split()[0] == line_list_3p[j][1]:
                line_list_3p[j].append(bus_coords[i].split()[1])
                line_list_3p[j].append(bus_coords[i].split()[2])
    for i in range(len(bus_coords)):
        for j in range(len(line_list_3p)):
            if bus_coords[i].split()[0] == line_list_3p[j][2]:
                line_list_3p[j].append(bus_coords[i].split()[1])
                line_list_3p[j].append(bus_coords[i].split()[2])

    return [line_list_1p, line_list_2p, line_list_3p]


def min_pu_value(l1,l2,l3,dssCircuit):

    min_pu_value = 2

    for i in range(len(l1)):
        if min_pu_value > V(l1[i][1],dssCircuit)[0]:
            min_pu_value = V(l1[i][1],dssCircuit)[0]

        if min_pu_value > V(l1[i][2],dssCircuit)[0]:
            min_pu_value = V(l1[i][2],dssCircuit)[0]

        if len(V(l1[i][1],dssCircuit)) == 4:
            if min_pu_value > V(l1[i][1],dssCircuit)[2]:
                min_pu_value = V(l1[i][1],dssCircuit)[2]

        if len(V(l1[i][2],dssCircuit)) == 4:
            if min_pu_value > V(l1[i][2],dssCircuit)[2]:
                min_pu_value = V(l1[i][2],dssCircuit)[2]

        if len(V(l1[i][1],dssCircuit)) == 6:
            if min_pu_value > V(l1[i][1],dssCircuit)[4]:
                min_pu_value = V(l1[i][1],dssCircuit)[4]

        if len(V(l1[i][2],dssCircuit)) == 6:
            if min_pu_value > V(l1[i][2],dssCircuit)[4]:
                min_pu_value = V(l1[i][2],dssCircuit)[4]

    for i in range(len(l2)):
        if min_pu_value > V(l2[i][1],dssCircuit)[0]:
            min_pu_value = V(l2[i][1],dssCircuit)[0]

        if min_pu_value > V(l2[i][2],dssCircuit)[0]:
            min_pu_value = V(l2[i][2],dssCircuit)[0]

        if len(V(l2[i][1],dssCircuit)) == 4:
            if min_pu_value > V(l2[i][1],dssCircuit)[2]:
                min_pu_value = V(l2[i][1],dssCircuit)[2]

        if len(V(l2[i][2],dssCircuit)) == 4:
            if min_pu_value > V(l2[i][2],dssCircuit)[2]:
                min_pu_value = V(l2[i][2],dssCircuit)[2]

        if len(V(l2[i][1],dssCircuit)) == 6:
            if min_pu_value > V(l2[i][1],dssCircuit)[4]:
                min_pu_value = V(l2[i][1],dssCircuit)[4]

        if len(V(l2[i][2],dssCircuit)) == 6:
            if min_pu_value > V(l2[i][2],dssCircuit)[4]:
                min_pu_value = V(l2[i][2],dssCircuit)[4]

    for i in range(len(l3)):
        if min_pu_value > V(l3[i][1],dssCircuit)[0]:
            min_pu_value = V(l3[i][1],dssCircuit)[0]

        if min_pu_value > V(l3[i][2],dssCircuit)[0]:
            min_pu_value = V(l3[i][2],dssCircuit)[0]

        if len(V(l3[i][1],dssCircuit)) == 4:
            if min_pu_value > V(l3[i][1],dssCircuit)[2]:
                min_pu_value = V(l3[i][1],dssCircuit)[2]

        if len(V(l3[i][2],dssCircuit)) == 4:
            if min_pu_value > V(l3[i][2],dssCircuit)[2]:
                min_pu_value = V(l3[i][2],dssCircuit)[2]

        if len(V(l3[i][1],dssCircuit)) == 6:
            if min_pu_value > V(l3[i][1],dssCircuit)[4]:
                min_pu_value = V(l3[i][1],dssCircuit)[4]

        if len(V(l3[i][2],dssCircuit)) == 6:
            if min_pu_value > V(l3[i][2],dssCircuit)[4]:
                min_pu_value = V(l3[i][2],dssCircuit)[4]

    return min_pu_value

def V(bus, dssCircuit):
    dssCircuit.SetActiveBus(bus)
    voltages = dssCircuit.ActiveBus.puVmagAngle
    return voltages

def C(element, dssCircuit):
    dssCircuit.SetActiveElement(element)
    currents = dssCircuit.ActiveElement.CurrentsMagAng
    return currents

def N(bus, dssCircuit):
    dssCircuit.SetActiveBus(bus)
    nodes = dssCircuit.ActiveBus.Nodes
    return nodes
