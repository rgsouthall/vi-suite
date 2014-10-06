import bpy, mathutils, math
from . import vi_func
from .livi_export import radgexport

try:
    import numpy
    np = 1
except:
    np = 0

def vigen(calc_op, li_calc, resapply, geonode, connode, simnode, geogennode, tarnode):
    scene = bpy.context.scene 
    simnode['Animation'] = 'Animated'
<<<<<<< local
    if not [ob for ob in scene.objects if ob.select and not ob.hide and ob.type == 'MESH'] and geogennode.oselmenu == 'Selected':
        calc_op.report({'ERROR'}, "No object is selected")
        return
    if geogennode.geomenu == 'Object':
        if geogennode.oselmenu == 'All':
            manipobs = [ob for ob in vi_func.retobjs('livig') if ob not in vi_func.retobjs('livic')]
        elif geogennode.oselmenu == 'Selected':   
            manipobs = [ob for ob in vi_func.retobjs('livig') if ob.select == True and ob not in vi_func.retobjs('livic')]
        else:
            manipobs = [ob for ob in vi_func.retobjs('livig') if ob.select == False and ob not in vi_func.retobjs('livic')]   
    
    elif geogennode.geomenu == 'Mesh':  
        if geogennode.oselmenu == 'All':
            manipobs = [ob for ob in vi_func.retobjs('livig')]
        elif geogennode.oselmenu == 'Selected':   
            manipobs = [ob for ob in vi_func.retobjs('livig') if ob.select == True]
        else:
            manipobs = [ob for ob in vi_func.retobjs('livig') if ob.select == False] 
       
        for ob in manipobs:
            vi_func.selobj(scene, ob)
            bpy.ops.object.mode_set(mode = 'EDIT')
            if ob.vertex_groups.get('genfaces'):            
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles()
                bpy.ops.mesh.select_all(action='DESELECT')
            else:
                ob.vertex_groups.new('genfaces')
                ob.vertex_groups.active = ob.vertex_groups['genfaces']
                if geogennode.mselmenu == 'Not Selected':
                    bpy.ops.mesh.select_all(action='INVERT')    
                elif geogennode.mselmenu == 'All':
                    bpy.ops.mesh.select_all(action='SELECT') 
                bpy.ops.object.vertex_group_assign()
            bpy.ops.object.mode_set(mode = 'OBJECT')
            ob['vgi'] = ob.vertex_groups['genfaces'].index
            
    for ob in vi_func.retobjs('livig'):
        ob.manip = 1 if ob in manipobs else 0
        vi_func.selobj(scene, ob)
        ob.animation_data_clear()
        ob.data.animation_data_clear()
        while ob.data.vertex_colors:
=======
    if not scene['livim']:
        calc_op.report({'ERROR'}, "No object has been set-up for generative manipulation")
        return
    else:
        liviom = scene['livim']
            
    for o in [bpy.data.objects[on] for on in scene['livig']]:
#        ob.manip = 1 if ob in [bpy.data.objects[o] for o in scene['genobs']] else 0
        vi_func.selobj(scene, o)
        o.animation_data_clear()
        o.data.animation_data_clear()
        while o.data.vertex_colors:
>>>>>>> other
            bpy.ops.mesh.vertex_color_remove()        
        while o.data.shape_keys:
            bpy.context.object.active_shape_key_index = 0
            bpy.ops.object.shape_key_remove(all=True)
#        if any([m.livi_sense for m in ob.data.materials]):
#            ob['licalc'] = 1
    scene.frame_set(scene.frame_start)
                    
    radgexport(calc_op, geonode, genframe = scene.frame_current)
    res = [li_calc(calc_op, simnode, connode, geonode, vi_func.livisimacc(simnode, connode), genframe = scene.frame_current)]
<<<<<<< local

    for ob in vi_func.retobjs('livic'):                 
        livicgeos = vi_func.retobjs('livic')
        if ob.get('licalc') == 1:
            vi_func.selobj(scene, ob)
            ob.keyframe_insert(data_path='["licalc"]')
            ob.keyframe_insert(data_path='["licalc"]', frame = scene.frame_current + 1)
=======
    livicgeos = vi_func.retobjs('livic')
    for o in [bpy.data.objects[on] for on in scene['livic']]:                 
        
        if o.name in scene['livic']:
            vi_func.selobj(scene, o)
            o.keyframe_insert(data_path='["licalc"]')
            o.keyframe_insert(data_path='["licalc"]', frame = scene.frame_current + 1)
>>>>>>> other
        else:
<<<<<<< local
            ob.manip = 0
        ob['licalc'] = vi_func.gentarget(tarnode, ob['oreslist']['{}'.format(scene.frame_current)])
=======
            scene['livim'].remove(o.name)
        if not vi_func.gentarget(tarnode, o['oreslist']['{}'.format(scene.frame_current)]):
            scene['livic'].remove(o.name)
>>>>>>> other
    
    for o in [bpy.data.objects[on] for on in scene['livim']]:
        if o.manip == 1 and geogennode.geomenu == 'Mesh':  
            vi_func.selobj(scene, o)
            bpy.ops.object.shape_key_add(from_mix = False)        
    
    while scene.frame_current < scene.frame_start + geogennode.steps + 1 and scene['livic']:        
        if scene.frame_current == scene.frame_start + 1 and geogennode.geomenu == 'Mesh':            
            for o in [bpy.data.objects[on] for on in scene['livim']]:  
                vi_func.selobj(scene, o)
                for face in o.data.polygons:
                    try:
                        face.select = True if all([o.data.vertices[v].groups[o['vgi']] for v in face.vertices]) else False
                    except:
                        face.select = False

                if geogennode.mmanmenu == '3': 
                    bpy.ops.object.mode_set(mode = 'EDIT')                    
                    bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv={"mirror":False}, TRANSFORM_OT_shrink_fatten={"value":0})
                    if o.vertex_groups.get('genexfaces'):
                        while len(o.vertex_groups) > 1:
                            o.vertex_groups.active_index = 1
                            bpy.ops.object.vertex_group_remove()
                    o.vertex_groups.new('genexfaces')
                    bpy.context.object.vertex_groups.active_index  = 1
                    bpy.ops.object.vertex_group_assign()
                    bpy.ops.object.mode_set(mode = 'OBJECT')                            
<<<<<<< local
                    ob['vgi'] = ob.vertex_groups['genexfaces'].index
                            
=======
                    o['vgi'] = o.vertex_groups['genexfaces'].index
                            
>>>>>>> other
        if scene.frame_current > scene.frame_start:              
<<<<<<< local
            for ob in manipobs:
                ob.keyframe_insert(data_path='["licalc"]')
                vi_func.selobj(scene, ob)  
                if ob.manip == 1 and geogennode.geomenu == 'Mesh':
=======
            for o in [bpy.data.objects[on] for on in liviom]:
                o.keyframe_insert(data_path='["licalc"]')
                vi_func.selobj(scene, o)  
                if o.name in scene['livim'] and geogennode.geomenu == 'Mesh':
>>>>>>> other
                    bpy.ops.object.shape_key_add(from_mix = False)
<<<<<<< local
                    ob.active_shape_key.name = 'gen-' + str(scene.frame_current)
                    modgeo(ob, geogennode, scene, scene.frame_current, scene.frame_start)   
                    for shape in ob.data.shape_keys.key_blocks:
=======
                    o.active_shape_key.name = 'gen-' + str(scene.frame_current)
                    modgeo(o, geogennode, scene, scene.frame_current, scene.frame_start)   
                    for shape in o.data.shape_keys.key_blocks:
>>>>>>> other
                        if "Basis" not in shape.name:
                            shape.value = 1 if shape.name == 'gen-{}'.format(scene.frame_current) else 0
<<<<<<< local
                            shape.keyframe_insert("value")                
                elif ob.manip == 1 and geogennode.geomenu == 'Object':
                    modgeo(ob, geogennode, scene, scene.frame_current, scene.frame_start)
                    ob.keyframe_insert(('location', 'rotation_euler', 'scale')[int(geogennode.omanmenu)])
                                        
            radgexport(calc_op, geonode, genframe = scene.frame_current, mo = [ob for ob in manipobs if ob.manip == 1])
=======
                            shape.keyframe_insert("value")                
                elif o.manip == 1 and geogennode.geomenu == 'Object':
                    modgeo(o, geogennode, scene, scene.frame_current, scene.frame_start)
                    o.keyframe_insert(('location', 'rotation_euler', 'scale')[int(geogennode.omanmenu)])
                                        
            radgexport(calc_op, geonode, genframe = scene.frame_current, mo = [bpy.data.objects[on] for on in scene['livim']])
>>>>>>> other
            res.append(li_calc(calc_op, simnode, connode, geonode, vi_func.livisimacc(simnode, connode), genframe = scene.frame_current))
            
<<<<<<< local
            for ob in vi_func.retobjs('livic'):
                ob['licalc'] = vi_func.gentarget(tarnode, ob['oreslist']['{}'.format(scene.frame_current)]) 
                ob.keyframe_insert(data_path='["licalc"]', frame = scene.frame_current + 1)
                ob.manip = ob['licalc'] if ob.manip == 1 else ob.manip
        
=======
            for o in [bpy.data.objects[on] for on in scene['livic']]:
                if not vi_func.gentarget(tarnode, o['oreslist']['{}'.format(scene.frame_current)]):
                    scene['livic'] = scene['livic'].remove(o.name) if scene['livic'].remove(o.name) else []
                    
                    if o.name in scene['livim']:
                        scene['livim'] = scene['livim'].remove(o.name) if scene['livim'].remove(o.name) else []
#                    o.manip = 0
                o.keyframe_insert(data_path='["licalc"]', frame = scene.frame_current + 1)
#                o.manip = ob['licalc'] if o.manip == 1 else o.manip

>>>>>>> other
        scene.frame_end = scene.frame_current + 1                        
        scene.frame_set(scene.frame_current + 1)
            
    scene.frame_end = scene.frame_end - 1  
    scene.fs = scene.frame_start    
    resapply(calc_op, res, 0, simnode, connode, geonode)
        
    for frame in vi_func.framerange(scene, 'Animation'):
        scene.frame_set(frame)
<<<<<<< local
        for geo in manipobs:
            if geogennode.geomenu == 'Mesh' and geo.data.shape_keys:
                for shape in geo.data.shape_keys.key_blocks:
=======
        for o in [bpy.data.objects[on] for on in liviom]:
            if geogennode.geomenu == 'Mesh' and o.data.shape_keys:
                for shape in o.data.shape_keys.key_blocks:
>>>>>>> other
                    if "Basis" not in shape.name:
                        shape.value = 1 if shape.name == 'gen-{}'.format(frame) else 0
                        if shape == o.data.shape_keys.key_blocks[-1] and frame > int(shape.name.split('-')[1]):
                            shape.value = 1
                        shape.keyframe_insert("value")
                    
    vi_func.vcframe('', scene, livicgeos, simnode['Animation'])            
    scene.frame_current = scene.frame_start       
        
def modgeo(o, geogennode, scene, fc, fs):            
    if geogennode.geomenu == 'Object':
        direc = (geogennode.x, geogennode.y, geogennode.z)
        if geogennode.omanmenu == '0':
            if fc == fs + 1:
                o.keyframe_insert('location', frame = fs)
            o.location += mathutils.Vector([(geogennode.extent/geogennode.steps) * xyz for xyz in direc])
            o.keyframe_insert('location', frame = fc)
        if geogennode.omanmenu == '1':
            if fc == fs + 1:
                o.keyframe_insert('rotation_euler', frame = fs)
            o.rotation_euler[0] += ((math.pi/180)*geogennode.extent/geogennode.steps) * direc[0]
            o.rotation_euler[1] += ((math.pi/180)*geogennode.extent/geogennode.steps) * direc[1]
            o.rotation_euler[2] += ((math.pi/180)*geogennode.extent/geogennode.steps) * direc[2]
            o.keyframe_insert('rotation_euler', frame = fc)
        if geogennode.omanmenu == '2':
            if fc == fs + 1:
                o.keyframe_insert('scale', frame = fs)
            o.scale += mathutils.Vector([(geogennode.extent/geogennode.steps) * xyz for xyz in direc])
            o.keyframe_insert('scale', frame = fc)
    else: 
        omw = o.matrix_world
        if fc > fs:
<<<<<<< local
            for face in ob.data.polygons:
                try:
                    if all([ob.data.vertices[v].groups[ob['vgi']] for v in face.vertices]):
                        direc = tuple(face.normal.normalized()) if geogennode.normal else (geogennode.x, geogennode.y, geogennode.z)
                        fcent = tuple(face.center)
                        for v in face.vertices:
                            if geogennode.mmanmenu in ('0', '3'):
                                ob.data.shape_keys.key_blocks['gen-{}'.format(fc)].data[v].co = ob.data.shape_keys.key_blocks['Basis'].data[v].co + mathutils.Vector([(-1, 1)[geogennode.direction == '0'] * (fc-fs) * (geogennode.extent/geogennode.steps) * d for d in direc])
                            elif geogennode.mmanmenu == '1':
                                mat_rot = mathutils.Matrix.Rotation(math.radians((fc-fs) * geogennode.extent/geogennode.steps), 4, face.normal)  if geogennode.normal else mathutils.Matrix.Rotation(math.radians((fc-fs) * geogennode.extent/geogennode.steps), 4, mathutils.Vector((geogennode.x, geogennode.y, geogennode.z)))
                                ob.data.shape_keys.key_blocks['gen-{}'.format(fc)].data[v].co = (mat_rot * (ob.data.shape_keys.key_blocks['Basis'].data[v].co - mathutils.Vector(fcent))) + mathutils.Vector(fcent)
                            elif geogennode.mmanmenu == '2':                            
                                mat_scl = mathutils.Matrix.Scale((1+(fc-fs)) * geogennode.extent/geogennode.steps, 4, mathutils.Vector([1 - fn for fn in face.normal]))  if geogennode.normal else mathutils.Matrix.Scale((1+(fc-fs)) * geogennode.extent/geogennode.steps, 4, mathutils.Vector((geogennode.x, geogennode.y, geogennode.z)))
#                                ob.data.shape_keys.key_blocks['gen-{}'.format(fc)].data[v].co = (mat_scl * (ob.data.shape_keys.key_blocks['Basis'].data[v].co - mathutils.Vector(fcent))) + mathutils.Vector(fcent)
                                ob.data.shape_keys.key_blocks['gen-{}'.format(fc)].data[v].co = [ob.data.shape_keys.key_blocks['Basis'].data[v].co[i] + (ob.data.shape_keys.key_blocks['Basis'].data[v].co[i] - fcent[i]) * (direc[i], 1 - direc[i])[geogennode.normal] * (1+(fc-fs)) * geogennode.extent/geogennode.steps for i in range(3)]
                except Exception as e:
                    print(e)        
=======
            for face in o.data.polygons:                
                if all([o.data.vertices[v].groups and o.data.vertices[v].groups[o['vgi']] for v in face.vertices]):
                    direc = [1- face.normal.normalized()[i] for i in range(3)] if geogennode.normal else (geogennode.x, geogennode.y, geogennode.z)
                    fcent = tuple(face.center)
                    for v in face.vertices:
                        if geogennode.mmanmenu in ('0', '3'):
                            o.data.shape_keys.key_blocks['gen-{}'.format(fc)].data[v].co = omw.inverted() * mathutils.Vector([(omw * o.data.shape_keys.key_blocks['gen-{}'.format(fc)].data[v].co)[i] + ((fc-fs) * (geogennode.extent/geogennode.steps) * direc[i]) for i in range(3)]) 
                        elif geogennode.mmanmenu == '1':
                            mat_rot = mathutils.Matrix.Rotation(math.radians((fc-fs) * geogennode.extent/geogennode.steps), 4, face.normal)  if geogennode.normal else mathutils.Matrix.Rotation(math.radians((fc-fs) * geogennode.extent/geogennode.steps), 4, mathutils.Vector((geogennode.x, geogennode.y, geogennode.z)))
                            o.data.shape_keys.key_blocks['gen-{}'.format(fc)].data[v].co = (mat_rot * (o.data.shape_keys.key_blocks['Basis'].data[v].co - mathutils.Vector(fcent))) + mathutils.Vector(fcent)
                        elif geogennode.mmanmenu == '2':                            
                            o.data.shape_keys.key_blocks['gen-{}'.format(fc)].data[v].co = [o.data.shape_keys.key_blocks['gen-{}'.format(fc)].data[v].co[i] + (geogennode.extent - 1)/geogennode.steps * (o.data.shape_keys.key_blocks['Basis'].data[v].co[i] - fcent[i]) * direc[i] * (fc-fs)  for i in range(3)]
     
>>>>>>> other
