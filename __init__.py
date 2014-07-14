bl_info = {
    "name": "VI-Suite",
    "author": "Ryan Southall",
    "version": (0, 1, 0),
    "blender": (2, 7, 0),
    "api":"",
    "location": "Node Editor & 3D View > Properties Panel",
    "description": "Radiance/EnergyPlus exporter and results visualiser",
    "warning": "This is a beta script. Some functionality is buggy",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}

if "bpy" in locals():
    import imp
    imp.reload(vi_node)
    imp.reload(vi_operators)
    imp.reload(vi_ui)
    imp.reload(vi_func)
    imp.reload(envi_mat)
else:
    from .vi_node import vinode_categories, envinode_categories
    from .envi_mat import envi_materials, envi_constructions
    from .vi_func import iprop, bprop, eprop, fprop, sprop, fvprop, sunpath1
    from .vi_operators import *
    from .vi_ui import *

import sys, os, platform, inspect, bpy, nodeitems_utils

epversion = "8-1-0"
addonpath = os.path.dirname(inspect.getfile(inspect.currentframe()))

if str(sys.platform) == 'darwin':
    if not hasattr(os.environ, 'RAYPATH'):
        if platform.architecture() == "64bit":
            os.environ["PATH"] = os.environ["PATH"] + ":/usr/local/radiance/bin:{}/osx/64:/Applications/EnergyPlus-{}/bin".format(addonpath, epversion)
        else:
             os.environ["PATH"] = os.environ["PATH"] + ":/usr/local/radiance/bin:{}/osx:/Applications/EnergyPlus-{}/bin".format(addonpath, epversion)
        os.environ["RAYPATH"] = "/usr/local/radiance/lib:{}/lib".format(addonpath)

if str(sys.platform) == 'linux':
    if not hasattr(os.environ, 'RAYPATH'):
        raddir =  '/usr/share/radiance' if os.path.isdir('/usr/share/radiance') else '/usr/local/radiance'
        os.environ["PATH"] = os.environ["PATH"] + ":{}/bin:{}/linux:/usr/local/EnergyPlus-{}/bin".format(raddir, addonpath, epversion)
        os.environ["RAYPATH"] = "{}/lib:{}/lib".format(raddir, addonpath)

elif str(sys.platform) == 'win32':
    if not hasattr(os.environ, 'RAYPATH'):
        if os.path.isdir(r"C:\Program Files (x86)\Radiance"):
            os.environ["PATH"] = os.environ["PATH"] + r";C:\Program Files (x86)\Radiance\bin;{}\windows;C:\EnergyPlusV{}".format(addonpath,epversion)
            os.environ["RAYPATH"] = r"C:\Program Files (x86)\Radiance\lib;{}\lib".format(addonpath)
        elif os.path.isdir(r"C:\Program Files\Radiance"):
            os.environ["PATH"] = os.environ["PATH"] + r";C:\Program Files\Radiance\bin;{}\windows;C:\EnergyPlusV{}".format(addonpath, epversion)
            os.environ["RAYPATH"] = "C:\Program Files\Radiance\lib;{}\lib".format(addonpath)
        else:
            print("Cannot find a valid Radiance directory. Please check that you have Radiance installed in either C:\Program Files(x86) (64bit windows) \
or C:\Program Files (32bit windows)")

matpath = addonpath+'/EPFiles/Materials/Materials.data'
epwpath = addonpath+'/EPFiles/Weather/'
envi_mats = envi_materials()
envi_cons = envi_constructions()

def matfunc(i):
    if i == 0:
        return [((brick, brick, 'Contruction type')) for brick in list(envi_mats.brick_dat.keys())]
    elif i == 1:
        return [((stone, stone, 'Contruction type')) for stone in list(envi_mats.stone_dat.keys())]
    elif i == 2:
        return [((metal, metal, 'Contruction type')) for metal in list(envi_mats.metal_dat.keys())]
    elif i == 3:
        return [((wood, wood, 'Contruction type')) for wood in list(envi_mats.wood_dat.keys())]
    elif i == 4:
        return [((gas, gas, 'Contruction type')) for gas in list(envi_mats.gas_dat.keys())]
    elif i == 5:
        return [((glass, glass, 'Contruction type')) for glass in list(envi_mats.glass_dat.keys())]
    elif i == 6:
        return [((concrete, concrete, 'Contruction type')) for concrete in list(envi_mats.concrete_dat.keys())]
    elif i == 7:
        return [((insulation, insulation, 'Contruction type')) for insulation in list(envi_mats.insulation_dat.keys())]
    elif i == 8:
        return [((wgas, wgas, 'Contruction type')) for wgas in list(envi_mats.wgas_dat.keys())]
    elif i == 9:
        return [((cladding, cladding, 'Contruction type')) for cladding in list(envi_mats.cladding_dat.keys())]
def confunc(i):
    if i == 0:
        return [((wallcon, wallcon, 'Contruction type')) for wallcon in list(envi_cons.wall_con.keys())]
    elif i == 1:
        return [((floorcon, floorcon, 'Contruction type')) for floorcon in list(envi_cons.floor_con.keys())]
    elif i == 2:
        return [((roofcon, roofcon, 'Contruction type')) for roofcon in list(envi_cons.roof_con.keys())]
    elif i == 3:
        return [((doorcon, doorcon, 'Contruction type')) for doorcon in list(envi_cons.door_con.keys())]
    elif i == 4:
        return [((windowcon, windowcon, 'Contruction type')) for windowcon in list(envi_cons.glaze_con.keys())]

(bricklist, stonelist, metallist, woodlist, gaslist, glasslist, concretelist, insullist, wgaslist, claddinglist) = [matfunc(i) for i in range(10)]
(wallconlist, floorconlist, roofconlist, doorconlist, glazeconlist) = [confunc(i) for i in range(5)]

def eupdate(self, context):
    inv = 0        
    for frame in range(context.scene.frame_start, context.scene.frame_end + 1):
        for o in [obj for obj in bpy.data.objects if obj.lires == 1]:
            if str(frame) in o['omax'].keys():
                maxo, mino = max(o['omax'].values()), min(o['omin'].values())
                if len(o['cverts']) == 0:
                    for i, fli in enumerate([(face, face.loop_indices) for face in o.data.polygons if face.select == True]):
                        for li in fli[1]:
                            vi = o.data.loops[li].vertex_index
                            o.data.shape_keys.key_blocks[str(frame)].data[vi].co = o.data.shape_keys.key_blocks['Basis'].data[vi].co + context.scene.vi_disp_3dlevel * (abs(inv - (o['oreslist'][str(frame)][i]-mino)/(maxo - mino)) * fli[0].normal)
                for vn, v in enumerate(o['cverts']):
                    o.data.shape_keys.key_blocks[str(frame)].data[v].co = o.data.shape_keys.key_blocks['Basis'].data[v].co + context.scene.vi_disp_3dlevel * (abs(inv - (o['oreslist'][str(frame)][vn]-mino)/(maxo - mino)) * o.data.vertices[v].normal)
                o.data.update()

def register():
    bpy.utils.register_module(__name__)
    Object = bpy.types.Object
    Scene = bpy.types.Scene
    Material = bpy.types.Material

# LiVi object properties

    Object.livi_merr = bprop("LiVi simple mesh export", "Boolean for simple mesh export", False)
    Object.ies_name = sprop("", "IES File", 1024, "")
    Object.ies_strength = fprop("", "Strength of IES lamp", 0, 1, 1)
    Object.ies_unit = eprop([("m", "Meters", ""), ("c", "Centimeters", ""), ("f", "Feet", ""), ("i", "Inches", "")], "", "Specify the IES file measurement unit", "m")
    Object.ies_colour = fvprop(3, "IES Colour",'IES Colour', [1.0, 1.0, 1.0], 'COLOR', 0, 1)
    Object.licalc = bprop("", "", False)
    Object.lires = bprop("", "", False)
    Object.limerr = bprop("", "", False)
    Object.manip = bprop("", "", False)

# EnVi zone definitions
    Object.envi_type = eprop([("0", "None", "None"), ("1", "Thermal", "Thermal Zone"), ("2", "Shading", "Shading Object")], "EnVi object type", "Specify the EnVi object type", "0")
# Heating defintions
    Object.envi_heat = iprop("W", "Heating", 0, 100000, 0)
    Object.envi_htsp = iprop(u'\u00b0'+"C", "Temperature", 0, 50, 20)
    Object.envi_htspsched = bprop("Schedule", "Create a thermostat level schedule", False)
    (Object.htspu1, Object.htspu2, Object.htspu3, Object.htspu4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (; separated for each 'For', comma separated for each day, space separated for each time value pair)")] * 4
    (Object.htspf1, Object.htspf2, Object.htspf3, Object.htspf4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (space separated): AllDays, Weekdays, Weekends, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, AllOtherDays")] * 4
    (Object.htspt1, Object.htspt2, Object.htspt3, Object.htspt4) = [bpy.props.IntProperty(name = "", default = 365, min = 1, max = 365)] * 4
# Cooling definitions
    Object.envi_cool = iprop("W", "Cooling", 0, 100000, 0)
    Object.envi_ctsp = iprop(u'\u00b0'+"C", "Temperature", 0, 50, 20)
    Object.envi_ctspsched = bprop("Schedule", "Create a thermostat level schedule", False)
    (Object.ctspu1, Object.ctspu2, Object.ctspu3, Object.ctspu4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (; separated for each 'For', comma separated for each day, space separated for each time value pair)")] * 4
    (Object.ctspf1, Object.ctspf2, Object.ctspf3, Object.ctspf4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (space separated): AllDays, Weekdays, Weekends, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, AllOtherDays")] * 4
    (Object.ctspt1, Object.ctspt2, Object.ctspt3, Object.ctspt4) = [bpy.props.IntProperty(name = "", default = 365, min = 1, max = 365)] * 4
#Occupancy definitions
    (Object.occu1, Object.occu2, Object.occu3, Object.occu4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (; separated for each 'For', comma separated for each day, space separated for each time value pair)")] * 4
    (Object.occf1, Object.occf2, Object.occf3, Object.occf4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (space separated): AllDays, Weekdays, Weekends, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, AllOtherDays")] * 4
    (Object.occt1, Object.occt2, Object.occt3, Object.occt4) = [bpy.props.IntProperty(name = "", default = 365, min = 1, max = 365)] * 4
    Object.envi_occwatts = iprop("W/p", "Watts per person", 70, 800, 90)
    Object.envi_asched = bprop("Schedule", "Create an activity level schedule", False)
    (Object.aoccu1, Object.aoccu2, Object.aoccu3, Object.aoccu4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (; separated for each 'For', comma separated for each day, space separated for each time value pair)")] * 4
    (Object.aoccf1, Object.aoccf2, Object.aoccf3, Object.aoccf4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (space separated): AllDays, Weekdays, Weekends, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, AllOtherDays")] * 4
    (Object.aocct1, Object.aocct2, Object.aocct3, Object.aocct4) = [bpy.props.IntProperty(name = "", default = 365, min = 1, max = 365)] * 4
    Object.envi_weff = fprop("Efficiency", "Work efficiency", 0, 1, 0.0)
    Object.envi_wsched = bprop("Schedule", "Create an activity level schedule", False)
    (Object.woccu1, Object.woccu2, Object.woccu3, Object.woccu4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (; separated for each 'For', comma separated for each day, space separated for each time value pair)")] * 4
    (Object.woccf1, Object.woccf2, Object.woccf3, Object.woccf4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (space separated): AllDays, Weekdays, Weekends, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, AllOtherDays")] * 4
    (Object.wocct1, Object.wocct2, Object.wocct3, Object.wocct4) = [bpy.props.IntProperty(name = "", default = 365, min = 1, max = 365)] * 4
    Object.envi_airv = fprop("Air velocity", "Average air velocity", 0, 1, 0.1)
    Object.envi_avsched = bprop("Schedule", "Create an air velocity schedule", False)
    (Object.avoccu1, Object.avoccu2, Object.avoccu3, Object.avoccu4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (; separated for each 'For', comma separated for each day, space separated for each time value pair)")] * 4
    (Object.avoccf1, Object.avoccf2, Object.avoccf3, Object.avoccf4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (space separated): AllDays, Weekdays, Weekends, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, AllOtherDays")] * 4
    (Object.avocct1, Object.avocct2, Object.avocct3, Object.avocct4) = [bpy.props.IntProperty(name = "", default = 365, min = 1, max = 365)] * 4

    Object.envi_cloth = fprop("Clothing", "Clothing level", 0, 1, 0.5)
    Object.envi_clsched = bprop("Schedule", "Create an clothing level schedule", False)
    (Object.coccu1, Object.coccu2, Object.coccu3, Object.coccu4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (; separated for each 'For', comma separated for each day, space separated for each time value pair)")] * 4
    (Object.coccf1, Object.coccf2, Object.coccf3, Object.coccf4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (space separated): AllDays, Weekdays, Weekends, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, AllOtherDays")] * 4
    (Object.cocct1, Object.cocct2, Object.cocct3, Object.cocct4) = [bpy.props.IntProperty(name = "", default = 365, min = 1, max = 365)] * 4

    Object.envi_occtype = eprop([("0", "None", "No occupancy"),("1", "Occupants", "Actual number of people"), ("2", "Person/m"+ u'\u00b2', "Number of people per squared metre floor area"),
                                              ("3", "m"+ u'\u00b2'+"/Person", "Floor area per person")], "", "The type of zone occupancy specification", "0")
    Object.envi_occsmax = fprop("Max", "Maximum level of occupancy that will occur in this schedule", 1, 500, 1)
    Object.envi_comfort = bprop("Comfort", "Enable comfor calculations for this space", False)

# Infiltration definitions
    Object.envi_inftype = eprop([("0", "None", "No infiltration"), ("1", 'Flow/Zone', "Absolute flow rate in m{}/s".format(u'\u00b3')), ("2", "Flow/Area", 'Flow in m{}/s per m{} floor area'.format(u'\u00b3', u'\u00b2')), 
                                 ("3", "Flow/ExteriorArea", 'Flow in m{}/s per m{} external surface area'.format(u'\u00b3', u'\u00b2')), ("4", "Flow/ExteriorWallArea", 'Flow in m{}/s per m{} external wall surface area'.format(u'\u00b3', u'\u00b2')), 
                                 ("4", "ACH", "ACH flow rate")], "", "The type of zone infiltration specification", "0")

    Object.envi_inflevel = fprop("Level", "Level of Infiltration", 0, 500, 0.001)
    Object.envi_infsched = bprop("Schedule", "Create an infiltration schedule", False)
    (Object.infu1, Object.infu2, Object.infu3, Object.infu4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (; separated for each 'For', comma separated for each day, space separated for each time value pair)")] * 4
    (Object.inff1, Object.inff2, Object.inff3, Object.inff4) =  [bpy.props.StringProperty(name = "", description = "Valid entries (space separated): AllDays, Weekdays, Weekends, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, AllOtherDays")] * 4
    (Object.inft1, Object.inft2, Object.inft3, Object.inft4) = [bpy.props.IntProperty(name = "", default = 365, min = 1, max = 365)] * 4

    
    Object.envi_occinftype = eprop([("0", "None", "No infiltration"), ("1", 'Flow/Zone', "Absolute flow rate in m{}/s".format(u'\u00b3')), ("2", "Flow/Area", 'Flow in m{}/s per m{} floor area'.format(u'\u00b3', u'\u00b2')), 
                                 ("3", "Flow/ExteriorArea", 'Flow in m{}/s per m{} external surface area'.format(u'\u00b3', u'\u00b2')), ("4", "Flow/ExteriorWallArea", 'Flow in m{}/s per m{} external wall surface area'.format(u'\u00b3', u'\u00b2')), 
                                 ("5", "ACH", "ACH flow rate"), ("6", "l/s/p", 'Litres per second per person')], "", "The type of zone infiltration specification", "0")

# LiVi material definitions
    Material.vi_shadow = bprop("VI Shadow", "Flag to signify whether the material represents a VI Shadow sensing surface", False)
    Material.livi_sense = bprop("LiVi Sensor", "Flag to signify whether the material represents a LiVi sensing surface", False)
    Material.livi_compliance = bprop("LiVi Compliance Surface", "Flag to siginify whether the material represents a LiVi compliance surface", False)
    Material.gl_roof = bprop("Glazed Roof", "Flag to siginify whether the communal area has a glazed roof", False)
    hspacetype = [('0', 'Public/Staff', 'Public/Staff area'), ('1', 'Patient', 'Patient area')]
    rspacetype = [('0', "Kitchen", "Kitchen space"), ('1', "Living/Dining/Study", "Living/Dining/Study area"), ('2', "Communal", "Non-residential or communal area")]
    respacetype = [('0', "Sales", "Sales space"), ('1', "Occupied", "Occupied space")]

    Material.hspacemenu = eprop(hspacetype, "", "Type of healthcare space", '0')
    Material.rspacemenu = eprop(rspacetype, "", "Type of residential space", '0')
    Material.respacemenu = eprop(respacetype, "", "Type of retail space", '0')

# EnVi material definitions

    Material.envi_con_type = eprop([("Wall", "Wall", "Wall construction"),("Floor", "Floor", "Floor construction"),("Roof", "Roof", "Roof construction"),("Window", "Window", "Window construction"), ("Door", "Door", "Door construction"),
                    ("Shading", "Shading", "Shading material"),("Aperture", "Aperture", "Airflow Aperture"),("None", "None", "Surface to be ignored")], "", "Specify the construction type", "None")
    Material.envi_boundary = bprop("On zone boundary", "Flag to siginify whether the material represents a zone boundary", False)
    Material.afsurface = bprop("Airflow surface", "Flag to siginify whether the material represents an airflow surface", False)
    Material.envi_aperture = eprop([("0", "External", "External facade airflow component", 0), ("1", "Internal", "Zone boundary airflow component", 1),], "", "Position of the airflow component", "0")
    Material.envi_con_makeup = eprop([("0", "Pre-set", "Construction pre-set"),("1", "Layers", "Custom layers"),("2", "Dummy", "Adiabatic")], "", "Pre-set construction of custom layers", "0")
    Material.envi_layero = eprop([("0", "None", "Not present"), ("1", "Database", "Select from databse"), ("2", "Custom", "Define custom material properties")], "", "Composition of the outer layer", "0")
    Material.envi_layerott = Material.envi_layer1tt = Material.envi_layer2tt = Material.envi_layer3tt = Material.envi_layer4tt = eprop(
                    [("0", "Glass", "Choose a material from the glass database"),("1", "Gas", "Choose a material from the gas database")], "", "Composition of the outer layer", "0")

    Material.envi_layeroto = Material.envi_layer1to = Material.envi_layer2to = Material.envi_layer3to = Material.envi_layer4to = eprop(
            [("0", "Brick", "Choose a material from the brick database"),("1", "Cladding", "Choose a material from the cladding database"), ("2", "Concrete", "Choose a material from the concrete database"),("3", "Metal", "Choose a material from the metal database"),
                   ("4", "Stone", "Choose a material from the stone database"),("5", "Wood", "Choose a material from the wood database"),
                   ("6", "Gas", "Choose a material from the gas database"),("7", "Insulation", "Choose a material from the insulation database")],"","Composition of the outer layer","0")

    Material.envi_layer1 = eprop([("0", "None", "Not present"),("1", "Database", "Select from databse"),("2", "Custom", "Define custom material properties")], "", "Composition of the next layer", "0")
    Material.envi_layer2 = eprop([("0", "None", "Not present"),("1", "Database", "Select from databse"),("2", "Custom", "Define custom material properties")],"","Composition of the next layer","0")
    Material.envi_layer3 = eprop([("0", "None", "Not present"),("1", "Database", "Select from databse"), ("2", "Custom", "Define custom material properties")],"","Composition of the next layer","0")
    Material.envi_layer4 = eprop([("0", "None", "Not present"),("1", "Database", "Select from databse"), ("2", "Custom", "Define custom material properties")], "", "Composition of the next layer", "0")
    Material.envi_export = bprop("Material Export", "Flag to tell EnVi to export this material", False)
    Material.envi_export_wallconlist = eprop(wallconlist, "Wall Constructions", "", wallconlist[0][0])
    Material.envi_export_floorconlist = eprop(floorconlist, "Floor Constructions",  "", floorconlist[0][0])
    Material.envi_export_roofconlist = eprop(roofconlist, "Roof Constructions",  "", roofconlist[0][0])
    Material.envi_export_doorconlist = eprop(doorconlist, "Door Constructions",  "", doorconlist[0][0])
    Material.envi_export_glazeconlist = eprop(glazeconlist, "Window Constructions",  "", glazeconlist[0][0])
    Material.envi_export_bricklist_lo = eprop(bricklist, "", "", bricklist[0][0])
    Material.envi_export_claddinglist_lo = eprop(claddinglist, "", "", claddinglist[0][0])
    Material.envi_export_stonelist_lo = eprop(stonelist, "",  "", stonelist[0][0])
    Material.envi_export_woodlist_lo = eprop(woodlist, "",  "", woodlist[0][0])
    Material.envi_export_metallist_lo = eprop(metallist, "",  "", metallist[0][0])
    Material.envi_export_gaslist_lo = eprop(gaslist, "",  "", gaslist[0][0])
    Material.envi_export_glasslist_lo = eprop(glasslist, "",  "", glasslist[0][0])
    Material.envi_export_concretelist_lo = eprop(concretelist, "",  "", concretelist[0][0])
    Material.envi_export_insulationlist_lo = eprop(insullist, "",  "", insullist[0][0])
    Material.envi_export_wgaslist_lo = eprop(wgaslist, "",  "", wgaslist[0][0])
    Material.envi_export_bricklist_l1 = eprop(bricklist, "",  "", bricklist[0][0])
    Material.envi_export_claddinglist_l1 = eprop(claddinglist, "", "", claddinglist[0][0])
    Material.envi_export_stonelist_l1 = eprop(stonelist, "",  "", stonelist[0][0])
    Material.envi_export_woodlist_l1 = eprop(woodlist, "",  "", woodlist[0][0])
    Material.envi_export_metallist_l1 = eprop(metallist, "",  "", metallist[0][0])
    Material.envi_export_gaslist_l1 = eprop(gaslist, "",  "", gaslist[0][0])
    Material.envi_export_glasslist_l1 = eprop(glasslist, "",  "", glasslist[0][0])
    Material.envi_export_concretelist_l1 = eprop(concretelist, "",  "", concretelist[0][0])
    Material.envi_export_insulationlist_l1 = eprop(insullist, "",  "", insullist[0][0])
    Material.envi_export_wgaslist_l1 = eprop(wgaslist, "",  "", wgaslist[0][0])
    Material.envi_export_bricklist_l2 = eprop(bricklist, "",  "", bricklist[0][0])
    Material.envi_export_claddinglist_l2 = eprop(claddinglist, "", "", claddinglist[0][0])
    Material.envi_export_stonelist_l2 = eprop(stonelist, "",  "", stonelist[0][0])
    Material.envi_export_woodlist_l2 = eprop(woodlist, "",  "", woodlist[0][0])
    Material.envi_export_metallist_l2 = eprop(metallist, "",  "", metallist[0][0])
    Material.envi_export_gaslist_l2 = eprop(gaslist, "",  "", gaslist[0][0])
    Material.envi_export_glasslist_l2 = eprop(glasslist, "",  "", glasslist[0][0])
    Material.envi_export_concretelist_l2 = eprop(concretelist, "",  "", concretelist[0][0])
    Material.envi_export_insulationlist_l2 = eprop(insullist, "",  "", insullist[0][0])
    Material.envi_export_wgaslist_l2 = eprop(wgaslist, "",  "", wgaslist[0][0])
    Material.envi_export_bricklist_l3 = eprop(bricklist, "",  "", bricklist[0][0])
    Material.envi_export_claddinglist_l3 = eprop(claddinglist, "", "", claddinglist[0][0])
    Material.envi_export_stonelist_l3 = eprop(stonelist, "",  "", stonelist[0][0])
    Material.envi_export_woodlist_l3 = eprop(woodlist, "",  "", woodlist[0][0])
    Material.envi_export_metallist_l3 = eprop(metallist, "",  "", metallist[0][0])
    Material.envi_export_gaslist_l3 = eprop(gaslist, "",  "", gaslist[0][0])
    Material.envi_export_glasslist_l3 = eprop(glasslist, "",  "", glasslist[0][0])
    Material.envi_export_concretelist_l3 = eprop(concretelist, "",  "", concretelist[0][0])
    Material.envi_export_insulationlist_l3 = eprop(insullist, "",  "", insullist[0][0])
    Material.envi_export_wgaslist_l3 = eprop(wgaslist, "",  "", wgaslist[0][0])
    Material.envi_export_bricklist_l4 = eprop(bricklist, "",  "", bricklist[0][0])
    Material.envi_export_claddinglist_l4 = eprop(claddinglist, "", "", claddinglist[0][0])
    Material.envi_export_stonelist_l4 = eprop(stonelist, "",  "", stonelist[0][0])
    Material.envi_export_woodlist_l4 = eprop(woodlist, "",  "", woodlist[0][0])
    Material.envi_export_metallist_l4 = eprop(metallist, "",  "", metallist[0][0])
    Material.envi_export_gaslist_l4 = eprop(gaslist, "",  "", gaslist[0][0])
    Material.envi_export_glasslist_l4 = eprop(glasslist, "",  "", glasslist[0][0])
    Material.envi_export_concretelist_l4 = eprop(concretelist, "",  "", concretelist[0][0])
    Material.envi_export_insulationlist_l4 = eprop(insullist, "",  "", insullist[0][0])
    Material.envi_export_wgaslist_l4 = eprop(wgaslist, "",  "", wgaslist[0][0])
    Material.envi_export_lo_name = sprop("Layer name", "Layer name", 0, "")
    Material.envi_export_l1_name = sprop("Layer name", "Layer name", 0, "")
    Material.envi_export_l2_name = sprop("Layer name", "Layer name", 0, "")
    Material.envi_export_l3_name = sprop("Layer name", "Layer name", 0, "")
    Material.envi_export_l4_name = sprop("Layer name", "Layer name", 0, "")
    Material.envi_export_lo_tc = fprop("Conductivity", "Thermal Conductivity", 0, 10, 0.5)
    Material.envi_export_l1_tc = fprop("Conductivity", "Thermal Conductivity", 0, 10, 0.5)
    Material.envi_export_l2_tc = fprop("Conductivity", "Thermal Conductivity", 0, 10, 0.5)
    Material.envi_export_l3_tc = fprop("Conductivity", "Thermal Conductivity", 0, 10, 0.5)
    Material.envi_export_l4_tc = fprop("Conductivity", "Thermal Conductivity", 0, 10, 0.5)
    Material.envi_export_lo_rough = eprop([("VeryRough", "VeryRough", "Roughness"), ("Rough", "Rough", "Roughness"), ("MediumRough", "MediumRough", "Roughness"),
                                                        ("MediumSmooth", "MediumSmooth", "Roughness"), ("Smooth", "Smooth", "Roughness"), ("VerySmooth", "VerySmooth", "Roughness")],
                                                        "Material surface roughness",
                                                        "specify the material rughness for convection calculations",
                                                        "Rough")
    Material.envi_export_l1_rough = eprop([("VeryRough", "VeryRough", "Roughness"), ("Rough", "Rough", "Roughness"), ("MediumRough", "MediumRough", "Roughness"),
                                                        ("MediumSmooth", "MediumSmooth", "Roughness"), ("Smooth", "Smooth", "Roughness"), ("VerySmooth", "VerySmooth", "Roughness")],
                                                        "Material surface roughness",
                                                        "specify the material rughness for convection calculations",
                                                        "Rough")
    Material.envi_export_l2_rough = eprop([("VeryRough", "VeryRough", "Roughness"), ("Rough", "Rough", "Roughness"), ("MediumRough", "MediumRough", "Roughness"),
                                                        ("MediumSmooth", "MediumSmooth", "Roughness"), ("Smooth", "Smooth", "Roughness"), ("VerySmooth", "VerySmooth", "Roughness")],
                                                        "Material surface roughness",
                                                        "specify the material rughness for convection calculations",
                                                        "Rough")
    Material.envi_export_l3_rough = eprop([("VeryRough", "VeryRough", "Roughness"), ("Rough", "Rough", "Roughness"), ("MediumRough", "MediumRough", "Roughness"),
                                                        ("MediumSmooth", "MediumSmooth", "Roughness"), ("Smooth", "Smooth", "Roughness"), ("VerySmooth", "VerySmooth", "Roughness")],
                                                        "Material surface roughness",
                                                        "specify the material rughness for convection calculations",
                                                        "Rough")
    Material.envi_export_l4_rough = eprop([("VeryRough", "VeryRough", "Roughness"), ("Rough", "Rough", "Roughness"), ("MediumRough", "MediumRough", "Roughness"),
                                                        ("MediumSmooth", "MediumSmooth", "Roughness"), ("Smooth", "Smooth", "Roughness"), ("VerySmooth", "VerySmooth", "Roughness")],
                                                        "Material surface roughness",
                                                        "specify the material rughness for convection calculations",
                                                        "Rough")
    Material.envi_export_lo_rho = fprop("Density", "Density (kg/m3)", 0, 10000, 1000)
    Material.envi_export_l1_rho = fprop("Density", "Density (kg/m3)", 0, 10000, 1000)
    Material.envi_export_l2_rho = fprop("Density", "Density (kg/m3)", 0, 10000, 1000)
    Material.envi_export_l3_rho = fprop("Density", "Density (kg/m3)", 0, 10000, 1000)
    Material.envi_export_l4_rho = fprop("Density", "Density (kg/m3)", 0, 10000, 1000)
    Material.envi_export_lo_shc = fprop("SHC", "Specific Heat Capacity (J/kgK)", 0, 10000, 1000)
    Material.envi_export_l1_shc = fprop("SHC", "Specific Heat Capacity (J/kgK)", 0, 10000, 1000)
    Material.envi_export_l2_shc = fprop("SHC", "Specific Heat Capacity (J/kgK)", 0, 10000, 1000)
    Material.envi_export_l3_shc = fprop("SHC", "Specific Heat Capacity (J/kgK)", 0, 10000, 1000)
    Material.envi_export_l4_shc = fprop("SHC", "Specific Heat Capacity (J/kgK)", 0, 10000, 1000)
    Material.envi_export_lo_thi = fprop("Thickness", "Thickness (mm)", 0, 10000, 100)
    Material.envi_export_l1_thi = fprop("Thickness", "Thickness (mm)", 0, 10000, 100)
    Material.envi_export_l2_thi = fprop("Thickness", "Thickness (mm)", 0, 10000, 100)
    Material.envi_export_l3_thi = fprop("Thickness", "Thickness (mm)", 0, 10000, 100)
    Material.envi_export_l4_thi = fprop("Thickness", "Thickness (mm)", 0, 10000, 100)
    Material.envi_export_lo_tab = fprop("TA", "Thermal Absorptance", 0, 1, 0.8)
    Material.envi_export_l1_tab = fprop("TA", "Thermal Absorptance", 0, 1, 0.8)
    Material.envi_export_l2_tab = fprop("TA", "Thermal Absorptance", 0, 1, 0.8)
    Material.envi_export_l3_tab = fprop("TA", "Thermal Absorptance", 0, 1, 0.8)
    Material.envi_export_l4_tab = fprop("TA", "Thermal Absorptance", 0, 1, 0.8)
    Material.envi_export_lo_sab = fprop("SA", "Solar Absorptance", 0, 1, 0.6)
    Material.envi_export_l1_sab = fprop("SA", "Solar Absorptance", 0, 1, 0.6)
    Material.envi_export_l2_sab = fprop("SA", "Solar Absorptance", 0, 1, 0.6)
    Material.envi_export_l3_sab = fprop("SA", "Solar Absorptance", 0, 1, 0.6)
    Material.envi_export_l4_sab = fprop("SA", "Solar Absorptance", 0, 1, 0.6)
    Material.envi_export_lo_vab = fprop("VA", "Visible Absorptance", 0, 1, 0.6)
    Material.envi_export_l1_vab = fprop("VA", "Visible Absorptance", 0, 1, 0.6)
    Material.envi_export_l2_vab = fprop("VA", "Visible Absorptance", 0, 1, 0.6)
    Material.envi_export_l3_vab = fprop("VA", "Visible Absorptance", 0, 1, 0.6)
    Material.envi_export_l4_vab = fprop("VA", "Visible Absorptance", 0, 1, 0.6)
    Material.envi_export_lo_odt = eprop([("SpectralAverage", "SpectralAverage", "Optical Data Type")], "Optical Data Type", "Optical Data Type", "SpectralAverage")
    Material.envi_export_l1_odt = eprop([("SpectralAverage", "SpectralAverage", "Optical Data Type")], "Optical Data Type", "Optical Data Type", "SpectralAverage")
    Material.envi_export_l2_odt = eprop([("SpectralAverage", "SpectralAverage", "Optical Data Type")], "Optical Data Type", "Optical Data Type", "SpectralAverage")
    Material.envi_export_l3_odt = eprop([("SpectralAverage", "SpectralAverage", "Optical Data Type")], "Optical Data Type", "Optical Data Type", "SpectralAverage")
    Material.envi_export_l4_odt = eprop([("SpectralAverage", "SpectralAverage", "Optical Data Type")], "Optical Data Type", "Optical Data Type", "SpectralAverage")
    Material.envi_export_lo_sds = eprop([("0", "", "Window Glass Spectral Data Set Name")], "Window Glass Spectral Data Set Name", "Window Glass Spectral Data Set Name", "0")
    Material.envi_export_l1_sds = eprop([("0", "", "Window Glass Spectral Data Set Name")], "Window Glass Spectral Data Set Name", "Window Glass Spectral Data Set Name", "0")
    Material.envi_export_l2_sds = eprop([("0", "", "Window Glass Spectral Data Set Name")], "Window Glass Spectral Data Set Name", "Window Glass Spectral Data Set Name", "0")
    Material.envi_export_l3_sds = eprop([("0", "", "Window Glass Spectral Data Set Name")], "Window Glass Spectral Data Set Name", "Window Glass Spectral Data Set Name", "0")
    Material.envi_export_l4_sds = eprop([("0", "", "Window Glass Spectral Data Set Name")], "Window Glass Spectral Data Set Name", "Window Glass Spectral Data Set Name", "0")
    Material.envi_export_lo_stn = fprop("STN", "Solar Transmittance at Normal Incidence", 0, 1, 0.9)
    Material.envi_export_l1_stn = fprop("STN", "Solar Transmittance at Normal Incidence", 0, 1, 0.9)
    Material.envi_export_l2_stn = fprop("STN", "Solar Transmittance at Normal Incidence", 0, 1, 0.9)
    Material.envi_export_l3_stn = fprop("STN", "Solar Transmittance at Normal Incidence", 0, 1, 0.9)
    Material.envi_export_l4_stn = fprop("STN", "Solar Transmittance at Normal Incidence", 0, 1, 0.9)
    Material.envi_export_lo_fsn = fprop("FSN", "Front Side Solar Reflectance at Normal Incidence", 0, 1, 0.075)
    Material.envi_export_l1_fsn = fprop("FSN", "Front Side Solar Reflectance at Normal Incidence", 0, 1, 0.075)
    Material.envi_export_l2_fsn = fprop("FSN", "Front Side Solar Reflectance at Normal Incidence", 0, 1, 0.075)
    Material.envi_export_l3_fsn = fprop("FSN", "Front Side Solar Reflectance at Normal Incidence", 0, 1, 0.075)
    Material.envi_export_l4_fsn = fprop("FSN", "Front Side Solar Reflectance at Normal Incidence", 0, 1, 0.075)
    Material.envi_export_lo_bsn = fprop("BSN", "Back Side Solar Reflectance at Normal Incidence", 0, 1, 0.075)
    Material.envi_export_l1_bsn = fprop("BSN", "Back Side Solar Reflectance at Normal Incidence", 0, 1, 0.075)
    Material.envi_export_l2_bsn = fprop("BSN", "Back Side Solar Reflectance at Normal Incidence", 0, 1, 0.075)
    Material.envi_export_l3_bsn = fprop("BSN", "Back Side Solar Reflectance at Normal Incidence", 0, 1, 0.075)
    Material.envi_export_l4_bsn = fprop("BSN", "Back Side Solar Reflectance at Normal Incidence", 0, 1, 0.075)
    Material.envi_export_lo_vtn = fprop("VTN", "Visible Transmittance at Normal Incidence", 0, 1, 0.9)
    Material.envi_export_l1_vtn = fprop("VTN", "Visible Transmittance at Normal Incidence", 0, 1, 0.9)
    Material.envi_export_l2_vtn = fprop("VTN", "Visible Transmittance at Normal Incidence", 0, 1, 0.9)
    Material.envi_export_l3_vtn = fprop("VTN", "Visible Transmittance at Normal Incidence", 0, 1, 0.9)
    Material.envi_export_l4_vtn = fprop("VTN", "Visible Transmittance at Normal Incidence", 0, 1, 0.9)
    Material.envi_export_lo_fvrn = fprop("FVRN", "Front Side Visible Reflectance at Normal Incidence", 0, 1, 0.08)
    Material.envi_export_l1_fvrn = fprop("FVRN", "Front Side Visible Reflectance at Normal Incidence", 0, 1, 0.08)
    Material.envi_export_l2_fvrn = fprop("FVRN", "Front Side Visible Reflectance at Normal Incidence", 0, 1, 0.08)
    Material.envi_export_l3_fvrn = fprop("FVRN", "Front Side Visible Reflectance at Normal Incidence", 0, 1, 0.08)
    Material.envi_export_l4_fvrn = fprop("FVRN", "Front Side Visible Reflectance at Normal Incidence", 0, 1, 0.08)
    Material.envi_export_lo_bvrn = fprop("BVRN", "Back Side Visible Reflectance at Normal Incidence", 0, 1, 0.08)
    Material.envi_export_l1_bvrn = fprop("BVRN", "Back Side Visible Reflectance at Normal Incidence", 0, 1, 0.08)
    Material.envi_export_l2_bvrn = fprop("BVRN", "Back Side Visible Reflectance at Normal Incidence", 0, 1, 0.08)
    Material.envi_export_l3_bvrn = fprop("BVRN", "Back Side Visible Reflectance at Normal Incidence", 0, 1, 0.08)
    Material.envi_export_l4_bvrn = fprop("BVRN", "Back Side Visible Reflectance at Normal Incidence", 0, 1, 0.08)
    Material.envi_export_lo_itn = fprop("ITN", "Infrared Transmittance at Normal Incidence", 0, 1, 0.0)
    Material.envi_export_l1_itn = fprop("ITN", "Infrared Transmittance at Normal Incidence", 0, 1, 0.0)
    Material.envi_export_l2_itn = fprop("ITN", "Infrared Transmittance at Normal Incidence", 0, 1, 0.0)
    Material.envi_export_l3_itn = fprop("ITN", "Infrared Transmittance at Normal Incidence", 0, 1, 0.0)
    Material.envi_export_l4_itn = fprop("ITN", "Infrared Transmittance at Normal Incidence", 0, 1, 0.0)
    Material.envi_export_lo_fie = fprop("FIE", "Front Side Infrared Hemispherical Emissivity", 0, 1, 0.84)
    Material.envi_export_l1_fie = fprop("FIE", "Front Side Infrared Hemispherical Emissivity", 0, 1, 0.84)
    Material.envi_export_l2_fie = fprop("FIE", "Front Side Infrared Hemispherical Emissivity", 0, 1, 0.84)
    Material.envi_export_l3_fie = fprop("FIE", "Front Side Infrared Hemispherical Emissivity", 0, 1, 0.84)
    Material.envi_export_l4_fie = fprop("FIE", "Front Side Infrared Hemispherical Emissivity", 0, 1, 0.84)
    Material.envi_export_lo_bie = fprop("BIE", "Back Side Infrared Hemispherical Emissivity", 0, 1, 0.84)
    Material.envi_export_l1_bie = fprop("BIE", "Back Side Infrared Hemispherical Emissivity", 0, 1, 0.84)
    Material.envi_export_l2_bie = fprop("BIE", "Back Side Infrared Hemispherical Emissivity", 0, 1, 0.84)
    Material.envi_export_l3_bie = fprop("BIE", "Back Side Infrared Hemispherical Emissivity", 0, 1, 0.84)
    Material.envi_export_l4_bie = fprop("BIE", "Back Side Infrared Hemispherical Emissivity", 0, 1, 0.84)
    Material.envi_shad_att = bprop("Attached", "Flag to specify shading attached to the building",False)

    # Scene parameters

    Scene.fs = iprop("Frame start", "Starting frame",0, 1000, 0)
    Scene.fe = iprop("Frame start", "End frame",0, 50000, 0)
    Scene.gfe = iprop("Frame start", "End frame",0, 50000, 0)
    Scene.cfe = iprop("Frame start", "End frame",0, 50000, 0)
    Scene.vipath = sprop("VI Path", "Path to files included with the VI-Suite ", 1024, addonpath)
    Scene.solday = bpy.props.IntProperty(name = "", description = "Day of year", min = 1, max = 365, default = 1, update=sunpath1)
    Scene.solhour = bpy.props.FloatProperty(name = "", description = "Time of day", min = 0, max = 24, default = 12, update=sunpath1)
    Scene.soldistance = bpy.props.IntProperty(name = "", description = "Sun path scale", min = 1, max = 5000, default = 100, update=sunpath1)
    Scene.hourdisp = bprop("", "",0)
    Scene.spupdate = bprop("", "",0)
#    Scene.latitude = bpy.props.FloatProperty(name="Latitude", description="Site Latitude", min=-90, max=90, default=52)
#    Scene.longitude = bpy.props.FloatProperty(name="Longitude", description="Site Longitude", min=-180, max=180, default=0)
    Scene.li_disp_panel = iprop("Display Panel", "Shows the Display Panel", -1, 2, 0)
    Scene.lic_disp_panel = bprop("", "",False)
    Scene.vi_disp_3d = bprop("VI 3D display", "Boolean for 3D results display",  False)
    Scene.vi_disp_3dlevel = bpy.props.FloatProperty(name = "", description = "Level of 3D result plane extrusion", min = 0, max = 500, default = 0, update = eupdate)
    Scene.vi_display = bprop("", "",False)
    Scene.sp_disp_panel = bprop("", "",False)
    Scene.wr_disp_panel = bprop("", "",False)
    Scene.ss_disp_panel = iprop("Display Panel", "Shows the Display Panel", -1, 2, 0)
    Scene.ss_leg_display = bprop("", "",False)
    Scene.en_disp_panel = bprop("", "",False)
    Scene.li_compliance = bprop("", "", False)
    Scene.vi_display_rp = bprop("", "", False)
    Scene.vi_leg_display = bprop("", "", False)
    Scene.vi_display_sel_only = bprop("", "", False)
    Scene.vi_display_vis_only = bprop("", "", False)
    Scene.vi_display_rp_fs = iprop("", "Point result font size", 4, 48, 9)
    Scene.vi_display_rp_fc = fvprop(4, "", "Font colour", [0.0, 0.0, 0.0, 1.0], 'COLOR', 0, 1)
    Scene.vi_display_rp_fsh = fvprop(4, "", "Font shadow", [0.0, 0.0, 0.0, 1.0], 'COLOR', 0, 1)
    Scene.li_projname = sprop("", "Name of the building project", 1024, '')
    Scene.li_assorg = sprop("", "Name of the assessing organisation", 1024, '')
    Scene.li_assind = sprop("", "Name of the assessing individual", 1024, '')
    Scene.li_jobno = sprop("", "Project job number", 1024, '')
    Scene.resnode = sprop("", "", 0, "")
    Scene.restree = sprop("", "", 0, "")

    nodeitems_utils.register_node_categories("Vi Nodes", vinode_categories)
    nodeitems_utils.register_node_categories("EnVi Nodes", envinode_categories)

def unregister():
    bpy.utils.unregister_module(__name__)
    nodeitems_utils.unregister_node_categories("Vi Nodes")
    nodeitems_utils.unregister_node_categories("EnVi Nodes")

