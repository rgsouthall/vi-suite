# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy, os, math, subprocess, datetime, bmesh, mathutils, shlex
from math import sin, cos, pi
from subprocess import PIPE, Popen
from .vi_func import clearscene, solarPosition, retobjs, radpoints, clearlayers, bmesh2mesh

def radgexport(export_op, node, **kwargs):
    scene = bpy.context.scene
    clearscene(scene, export_op)
    frames = range(node['Options']['fs'], node['Options']['fe'] + 1)
    scene['liparams']['cp'] = node.cpoint
    if bpy.context.active_object and not bpy.context.active_object.layers[scene.active_layer]:
        export_op.report({'INFO'}, "Active geometry is not on the active layer. You may need to lock layers.")
    geooblist, caloblist, lightlist = retobjs('livig'), retobjs('livic'), retobjs('livil')
    scene['liparams']['livig'], scene['liparams']['livic'], scene['liparams']['livil'] = [o.name for o in geooblist], [o.name for o in caloblist], [o.name for o in lightlist]
    eolist = set(geooblist + caloblist)
    mats = set([item for sublist in [o.data.materials for o in eolist] for item in sublist])
    
    for o in eolist:        
        if not node.animated:
            o.animation_data_clear()
            o.data.animation_data_clear()
#        if o.get('rtpoints'):
#            del o['rtpoints']
#            del o['lisenseareas']
        for k in o.keys():
            del o[k]
        if o in caloblist:
            o['rtpoints'] = {}
            o['lisenseareas'] = {}
        
    
    for frame in frames:
        scene.frame_set(frame)
        mradfile =  "# Materials \n\n" + "".join([m.radmat(scene) for m in mats])
        bpy.ops.object.select_all(action='DESELECT')
        tempmatfilename = scene['viparams']['filebase']+".tempmat"
        with open(tempmatfilename, "w") as tempmatfile:
            tempmatfile.write(mradfile)

        # Geometry export routine

        gradfile = "# Geometry \n\n"

        for o in eolist:
            bm = bmesh.new()
            tempmesh = o.to_mesh(scene = scene, apply_modifiers = True, settings = 'PREVIEW')
            bm.from_mesh(tempmesh)
            bpy.data.meshes.remove(tempmesh)
            bm.transform(o.matrix_world)
            bm.normal_update() 
            gradfile += bmesh2mesh(scene, bm, o, frame, tempmatfilename)
                        
            if o in caloblist:
                geom = (bm.faces, bm.verts)[int(node.cpoint)]
                if frame == frames[0]:
                    clearlayers(bm, 'a')                                    
                    geom.layers.int.new('cindex')
                    o['cpoint'] = node.cpoint
                geom.layers.string.new('rt{}'.format(frame))
                    
                if o in caloblist: 
                    o.rtpoints(bm, node.offset, str(frame))
                    bm.transform(o.matrix_world.inverted())
                    bm.to_mesh(o.data)
                        
            bm.free()
            
    # Lights export routine

        lradfile = "# Lights \n\n"
        for o in lightlist:
            iesname = os.path.splitext(os.path.basename(o.ies_name))[0]
            if os.path.isfile(o.ies_name):
                iescmd = "ies2rad -t default -m {0} -c {1[0]:.3f} {1[1]:.3f} {1[2]:.3f} -p {2} -d{3} -o {4}-{5} {6}".format(o.ies_strength, o.ies_colour, scene['liparams']['lightfilebase'], o.ies_unit, iesname, frame, o.ies_name)
                subprocess.call(iescmd.split())
                if o.type == 'LAMP':
                    if o.parent:
                        o = o.parent
                    lradfile += '!xform -rx {0[0]:.3f} -ry {0[1]:.3f} -rz {0[2]:.3f} -t {1[0]:.3f} {1[1]:.3f} {1[2]:.3f} "{2}.rad"\n\n'.format([(180/pi)*o.rotation_euler[i] for i in range(3)], o.location, os.path.join(scene['liparams']['lightfilebase'], iesname+"-{}".format(frame)))
                elif o.type == 'MESH':
                    for face in o.data.polygons:
                        lradfile += '!xform -rx {0[0]:.3f} -ry {0[1]:.3f} -rz {0[2]:.3f} -t {1[0]:.3f} {1[1]:.3f} {1[2]:.3f} "{2}"{3}'.format([(180/pi)*o.rotation_euler[i] for i in range(3)], o.matrix_world * face.center, os.path.join(scene['liparams']['lightfilebase'], iesname+"-{}.rad".format(frame)), ('\n', '\n\n')[face == o.data.polygons[-1]])
            elif iesname:
                export_op.report({'ERROR'}, 'The IES file associated with {} cannot be found'.format(o.name))

        sradfile = "# Sky \n\n"
        node['Text'][str(frame)] = mradfile+gradfile+lradfile+sradfile

def sunexport(scene, node, locnode, frame):
    if locnode and node.contextmenu == 'Basic':        
        simtime = node.starttime + frame*datetime.timedelta(seconds = 3600*node.interval)
        solalt, solazi, beta, phi = solarPosition(simtime.timetuple()[7], simtime.hour + (simtime.minute)*0.016666, scene.latitude, scene.longitude)
        gsrun = Popen("gensky -ang {} {} {} -t {}".format(solalt, solazi, node['skytypeparams'], node.turb).split(), stdout = PIPE)           
    else:
        gsrun = Popen("gensky -ang {} {} {}".format(45, 0, node['skytypeparams']).split(), stdout = PIPE)
    return gsrun.stdout.read().decode()

def hdrexport(scene, f, frame, node, skytext):
    with open('{}-{}sky.oct'.format(scene['viparams']['filebase'], frame), 'w') as skyoct:
        Popen('oconv -w -'.split(), stdin = PIPE, stdout = skyoct).communicate(input = skytext.encode('utf-8'))
    with open(os.path.join(scene['viparams']['newdir'], str(frame)+".hdr"), 'w') as hdrfile:
        rpictcmd = "rpict -vta -vp 0 0 0 -vd 0 1 0 -vu 0 0 1 -vh 360 -vv 360 -x 1500 -y 1500 {}-{}sky.oct".format(scene['viparams']['filebase'], frame)
        Popen(rpictcmd.split(), stdout = hdrfile).communicate()
    cntrun = Popen('cnt 750 1500'.split(), stdout = PIPE)
    rcalccmd = 'rcalc -f {} -e XD=1500;YD=750;inXD=0.000666;inYD=0.001333'.format(os.path.join(scene.vipath, 'Radfiles', 'lib', 'latlong.cal'))
    rcalcrun = Popen(rcalccmd.split(), stdin = cntrun.stdout, stdout = PIPE)
    rtracecmd = 'rtrace -n {} -x 1500 -y 750 -fac {}-{}sky.oct'.format(scene['viparams']['nproc'], scene['viparams']['filebase'], frame)
    with open('{}p.hdr'.format(os.path.join(scene['viparams']['newdir'], str(frame))), 'w') as hdrim:
        Popen(rtracecmd.split(), stdin = rcalcrun.stdout, stdout = hdrim).communicate()
    if '{}p.hdr'.format(frame) not in bpy.data.images:
        bpy.data.images.load(os.path.join(scene['viparams']['newdir'], "{}p.hdr".format(frame)))
    else:
        bpy.data.images['{}p.hdr'.format(frame)].reload()

def skyexport(sn):
    skytext = "4 .8 .8 1 0\n\n" if sn < 3 else "4 1 1 1 0\n\n"
    return "\nskyfunc glow sky_glow\n0\n0\n" + skytext + "sky_glow source sky\n0\n0\n4 0 0 1  180\n\n"

def createradfile(scene, frame, export_op, simnode):
    radtext = ''
    links = (list(simnode.inputs['Geometry in'].links[:]) + list(simnode.inputs['Context in'].links[:]))
    
    for link in links:
        if str(frame) in link.from_node['Text']:
            radtext += link.from_node['Text'][str(frame)]
        elif frame < min([int(k) for k in link.from_node['Text'].keys()]):
            radtext += link.from_node['Text'][str(min([int(k) for k in link.from_node['Text'].keys()]))]
        elif frame > max([int(k) for k in link.from_node['Text'].keys()]):
            radtext += link.from_node['Text'][str(max([int(k) for k in link.from_node['Text'].keys()]))]

    simnode['radfiles'][str(frame)] = radtext

def createoconv(scene, frame, export_op, simnode, **kwargs):
    fbase = "{0}-{1}".format(scene['viparams']['filebase'], frame)
    with open("{}.oct".format(fbase), "w") as octfile:
        Popen("oconv -w -".split(), stdin = PIPE, stdout = octfile).communicate(input = simnode['radfiles'][str(frame)].encode('utf-8'))

def spfc(self):
    scene = bpy.context.scene
    if not scene['viparams'].get('newframe'):
        scene['viparams']['newframe'] = 1
    else:
        scene['viparams']['newframe'] = 0
        scene.frame_set(scene.frame_current)
        
    if scene['viparams']['resnode'] == 'VI Sun Path':
        spoblist = {ob.get('VIType'):ob for ob in scene.objects if ob.get('VIType') in ('Sun', 'SPathMesh')}
        beta, phi = solarPosition(scene.solday, scene.solhour, scene.latitude, scene.longitude)[2:]
        if scene.world.use_nodes == False:
            scene.world.use_nodes = True
        nt = bpy.data.worlds[0].node_tree
        if nt and nt.nodes.get('Sky Texture'):
            scene.world.node_tree.nodes['Sky Texture'].sun_direction = -sin(phi), -cos(phi), sin(beta)

        for ob in scene.objects:
            if ob.get('VIType') == 'Sun':
                ob.rotation_euler = pi * 0.5 - beta, 0, -phi 
                ob.location.z = spoblist['SPathMesh'].location.z + 100 * sin(beta)                
                ob.location.x = spoblist['SPathMesh'].location.x -(100**2 - (spoblist['Sun'].location.z-spoblist['SPathMesh'].location.z)**2)**0.5 * sin(phi)
                ob.location.y = spoblist['SPathMesh'].location.y -(100**2 - (spoblist['Sun'].location.z-spoblist['SPathMesh'].location.z)**2)**0.5 * cos(phi)
                
                if ob.data.node_tree:
                    for blnode in [blnode for blnode in ob.data.node_tree.nodes if blnode.bl_label == 'Blackbody']:
                        blnode.inputs[0].default_value = 2500 + 3000*sin(beta)**0.5
                    for emnode in [emnode for emnode in ob.data.node_tree.nodes if emnode.bl_label == 'Emission']:
                        emnode.inputs[1].default_value = 10 * sin(beta)

            elif ob.get('VIType') == 'SkyMesh':
                ont = ob.data.materials['SkyMesh'].node_tree
                if ont and ont.nodes.get('Sky Texture'):
                    ont.nodes['Sky Texture'].sun_direction = sin(phi), -cos(phi), sin(beta)

            elif ob.get('VIType') == 'SunMesh':
                ob.location = (0, 0, 0)
                if ob.data.materials[0].node_tree:
                    for smblnode in [smblnode for smblnode in ob.data.materials[0].node_tree.nodes if ob.data.materials and smblnode.bl_label == 'Blackbody']:
                        smblnode.inputs[0].default_value = 2500 + 3000*sin(beta)**0.5
    else:
        return
    
def cyfc1(self):
    scene = bpy.context.scene        
    if 'LiVi' in scene['viparams']['resnode'] or 'Shadow' in scene['viparams']['resnode']:
        for material in [m for m in bpy.data.materials if m.use_nodes and m.mattype == '1']:
            try:
                if any([node.bl_label == 'Attribute' for node in material.node_tree.nodes]):
                    material.node_tree.nodes["Attribute"].attribute_name = str(scene.frame_current)
            except Exception as e:
                print(e, 'Something wrong with changing the material attribute name')    
        
def genbsdf(scene, export_op, o): 
    bsdfmats = [mat for mat in o.data.materials if mat.radmatmenu == '8']
    if bsdfmats:
        mat = bsdfmats[0]
        mat['bsdf'] = {} 
    else:
        export_op.report({'ERROR'}, '{} does not have a BSDF material attached'.format(o.name))

    bm = bmesh.new()    
    bm.from_mesh(o.data) 
    bm.transform(o.matrix_world)
    bm.normal_update()
    bsdffaces = [face for face in bm.faces if o.data.materials[face.material_index].radmatmenu == '8']    
    
    if bsdffaces:
        fvec = bsdffaces[0].normal
        mat['bsdf']['normal'] = '{0[0]} {0[1]} {0[2]}'.format(fvec)
    else:
        export_op.report({'ERROR'}, '{} does not have a BSDF material associated with any faces'.format(o.name))
        return
    
    zvec, xvec = mathutils.Vector((0, 0, 1)), mathutils.Vector((1, 0, 0))
    svec = fvec * mathutils.Matrix.Rotation(1.5 * math.pi, 4, zvec)
    bm.faces.ensure_lookup_table()
    bsdfrotz = mathutils.Matrix.Rotation(mathutils.Vector.angle(fvec, zvec), 4, mathutils.Vector.cross(fvec, zvec))
    bm.transform(bsdfrotz)
    bsdfrotx = mathutils.Matrix.Rotation(mathutils.Vector.angle(svec, xvec), 4, mathutils.Vector.cross(svec, xvec))
    bm.transform(bsdfrotx)
    vposis = list(zip(*[v.co[:] for v in bm.verts]))
    (maxx, maxy, maxz) = [max(p) for p in vposis]
    (minx, miny, minz) = [min(p) for p in vposis]
    bsdftrans = mathutils.Matrix.Translation(mathutils.Vector((-(maxx + minx)/2, -(maxy + miny)/2, -maxz)))
    bm.transform(bsdftrans)
    mradfile = ''.join([m.radmat(scene) for m in o.data.materials if m.radmatmenu != '8'])                  
    gradfile = radpoints(o, [face for face in bm.faces if o.data.materials and face.material_index < len(o.data.materials) and o.data.materials[face.material_index].radmatmenu != '8'], 0)
    bm.free()  
    bsdfsamp = o.li_bsdf_ksamp if o.li_bsdf_tensor == ' ' else 2**(int(o.li_bsdf_res) * 2) * int(o.li_bsdf_tsamp) 
#    bsdfxml = os.path.join(scene['viparams']['newdir'], 'bsdfs', '{}.xml'.format(mat.name))
    gbcmd = "genBSDF +geom meter -r '{}' {} {} -c {} {} -n {}".format(o.li_bsdf_rcparam,  o.li_bsdf_tensor, (o.li_bsdf_res, ' ')[o.li_bsdf_tensor == ' '], bsdfsamp, o.li_bsdf_direc, scene['viparams']['nproc'])
#    with open(bsdfxml, 'w') as bsdfwrite:        
    mat['bsdf']['xml'] = Popen(shlex.split(gbcmd), stdin = PIPE, stdout = PIPE).communicate(input = (mradfile+gradfile).encode('utf-8'))[0].decode()
#    mat['bsdf']['xml'] = bsdfxml
    mat['bsdf']['proxy_depth'] = -minz
    

    