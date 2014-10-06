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

import bpy, os, subprocess, colorsys, datetime, mathutils
from subprocess import PIPE, Popen, STDOUT
from . import vi_func
from . import livi_export

try:
    import numpy
    np = 1
except:
    np = 0

def radfexport(scene, export_op, connode, geonode, frames):
    for frame in frames:
<<<<<<< local
        livi_export.fexport(scene, frame, export_op, connode, geonode, pause = 1)

def rad_prev(prev_op, simnode, connode, geonode, simacc):    
    scene = bpy.context.scene    
    if os.path.isfile("{}-{}.rad".format(geonode.filebase, scene.frame_current)):
        cam = scene.camera
        if cam != None:
            cang = '180 -vth' if connode.analysismenu == '3' else cam.data.angle*180/pi
            vv = 180 if connode.analysismenu == '3' else cang * scene.render.resolution_y/scene.render.resolution_x
            rvucmd = "rvu -w -n {0} -vv {1} -vh {2} -vd {3[0][2]:.3f} {3[1][2]:.3f} {3[2][2]:.3f} -vp {4[0]:.3f} {4[1]:.3f} {4[2]:.3f} {5} {6}-{7}.oct &".format(geonode.nproc, vv, cang, -1*cam.matrix_world, cam.location, simnode['radparams'], geonode.filebase, scene.frame_current)
            rvurun = Popen(rvucmd, shell = True, stdout=PIPE, stderr=STDOUT)
            for l,line in enumerate(rvurun.stdout):            
                if 'octree' in line.decode() or 'mesh' in line.decode():
                    prev_op.report({'ERROR'}, "Something wrong with the Radiance input files. Try rerunning the geometry and context export")
                    return
        else:
            prev_op.report({'ERROR'}, "There is no camera in the scene. Radiance preview will not work")
    else:
        prev_op.report({'ERROR'},"Missing export file. Make sure you have exported the scene or that the current frame is within the exported frame range.")
=======
        livi_export.fexport(scene, frame, export_op, connode, geonode, pause = 1)
>>>>>>> other

def li_calc(calc_op, simnode, connode, geonode, simacc, **kwargs): 
    scene = bpy.context.scene
    frames = range(scene.fs, scene.fe + 1) if not kwargs.get('genframe') else [kwargs['genframe']]
<<<<<<< local
    os.chdir(geonode.newdir)
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode = 'OBJECT')
    if os.lstat(geonode.filebase+".rtrace").st_size == 0:
=======
    os.chdir(scene['viparams']['newdir'])
    if os.lstat("{}.rtrace".format(scene['viparams']['filebase'])).st_size == 0:
>>>>>>> other
        calc_op.report({'ERROR'},"There are no materials with the livi sensor option enabled")
    else:
<<<<<<< local
        if np == 1:
            res, svres = numpy.zeros([len(frames), geonode['reslen']]), numpy.zeros([len(frames), geonode['reslen']])
        else:
            res, svres = [[[0 for p in range(geonode['reslen'])] for x in range(len(frames))] for x in range(2)]
=======
        if np == 1:
            (res, svres) = (numpy.zeros([len(frames), geonode['reslen']]), numpy.zeros([len(frames), geonode['reslen']])) if np == 1 else ([[[0 for p in range(geonode['reslen'])] for x in range(len(frames))] for x in range(2)])
>>>>>>> other

        for frame in frames:            
            findex = frame - scene.fs if not kwargs.get('genframe') else 0
            if connode.bl_label in ('LiVi Basic', 'LiVi Compliance') or (connode.bl_label == 'LiVi CBDM' and int(connode.analysismenu) < 2):
<<<<<<< local
                if os.path.isfile("{}-{}.af".format(geonode.filebase, frame)):
                    subprocess.call("{} {}-{}.af".format(geonode.rm, geonode.filebase, frame), shell=True)
                rtcmd = "rtrace -n {0} -w {1} -faa -h -ov -I {2}-{3}.oct  < {2}.rtrace {4}".format(geonode.nproc, simnode['radparams'], geonode.filebase, frame, connode['simalg']) #+" | tee "+lexport.newdir+lexport.fold+self.simlistn[int(lexport.metric)]+"-"+str(frame)+".res"
                rtrun = Popen(rtcmd, shell = True, stdout=PIPE, stderr=STDOUT)
                with open(os.path.join(geonode.newdir, connode['resname']+"-"+str(frame)+".res"), 'w') as resfile:
=======
                if os.path.isfile("{}-{}.af".format(scene['viparams']['filebase'], frame)):
                    subprocess.call("{} {}-{}.af".format(scene['viparams']['rm'], scene['viparams']['filebase'], frame), shell=True)
                rtcmd = "rtrace -n {0} -w {1} -faa -h -ov -I {2}-{3}.oct  < {2}.rtrace {4}".format(scene['viparams']['nproc'], simnode['radparams'], scene['viparams']['filebase'], frame, connode['simalg']) #+" | tee "+lexport.newdir+lexport.fold+self.simlistn[int(lexport.metric)]+"-"+str(frame)+".res"
                rtrun = Popen(rtcmd, shell = True, stdout=PIPE, stderr=STDOUT)                
                with open(os.path.join(scene['viparams']['newdir'], connode['resname']+"-{}.res".format(frame)), 'w') as resfile:
>>>>>>> other
                    for l,line in enumerate(rtrun.stdout):
<<<<<<< local
                        if 'octree' in line.decode() or 'mesh' in line.decode():
                            print(line.decode() + ' rerunning export')
                            resfile.close()
                            radfexport(scene, calc_op, connode, geonode, frames)
                            if kwargs.get('genframe'):
                                res = li_calc(calc_op, simnode, connode, geonode, simacc, genframe = kwargs.get('genframe'))
                                return(res)                                
                            else:
                                li_calc(calc_op, simnode, connode, geonode, simacc)
                                return
                        res[findex][l] = float(line.decode())
                    resfile.write("{}".format(res).strip("]").strip("["))
=======
                        res[findex][l] = eval(line.decode())                
                        resfile.write(line.decode())
>>>>>>> other
                
            if connode.bl_label == 'LiVi Compliance' and connode.analysismenu in ('0', '1'):
                if connode.analysismenu in ('0', '1'):
<<<<<<< local
                    svcmd = "rtrace -n {0} -w {1} -h -ov -I -af {2}-{3}.af {2}-{3}.oct  < {2}.rtrace {4}".format(geonode.nproc, '-ab 1 -ad 8192 -aa 0 -ar 512 -as 1024 -lw 0.0002', geonode.filebase, frame, connode['simalg']) #+" | tee "+lexport.newdir+lexport.fold+self.simlistn[int(lexport.metric)]+"-"+str(frame)+".res"
                    svrun = Popen(svcmd, shell = True, stdout=PIPE, stderr=STDOUT)
                    with open(os.path.join(geonode.newdir,'skyview'+"-"+str(frame)+".res"), 'w') as svresfile:
=======
                    svcmd = "rtrace -n {0} -w {1} -h -ov -I -af {2}-{3}.af {2}-{3}.oct  < {2}.rtrace {4}".format(scene['viparams']['nproc'], '-ab 1 -ad 8192 -aa 0 -ar 512 -as 1024 -lw 0.0002', scene['viparams']['filebase'], frame, connode['simalg']) #+" | tee "+lexport.newdir+lexport.fold+self.simlistn[int(lexport.metric)]+"-"+str(frame)+".res"
                    svrun = Popen(svcmd, shell = True, stdout=PIPE, stderr=STDOUT)                  
                    with open(os.path.join(scene['viparams']['newdir'],'skyview'+"-"+str(frame)+".res"), 'w') as svresfile:
>>>>>>> other
                        for sv,line in enumerate(svrun.stdout):
                            svres[findex][sv] = eval(line.decode())
                            svresfile.write(line.decode())

            if connode.bl_label == 'LiVi CBDM' and int(connode.analysismenu) > 1:
                if connode.sourcemenu == '1':
                    connode['vecvals'], vals = vi_func.mtx2vals(open(connode.mtxname, "r").readlines(), datetime.datetime(2010, 1, 1).weekday(), '')
                hours = 0
<<<<<<< local
                sensarray = [[0 for x in range(146)] for y in range(geonode['reslen'])] if np == 0 else numpy.zeros([geonode['reslen'], 146])
                oconvcmd = "oconv -w - > {0}-ws.oct".format(geonode.filebase)
=======
                sensarray = [[0 for x in range(146)] for y in range(geonode['reslen'])] if np == 0 else numpy.zeros([geonode['reslen'], 146])
                oconvcmd = "oconv -w - > {0}-ws.oct".format(scene['viparams']['filebase'])
>>>>>>> other
                Popen(oconvcmd, shell = True, stdin = PIPE, stdout=PIPE, stderr=STDOUT).communicate(input = (connode['whitesky']+geonode['radfiles'][frame]).encode('utf-8'))
<<<<<<< local
                senscmd = geonode.cat+geonode.filebase+".rtrace | rcontrib -w  -h -I -fo -bn 146 "+simnode['radparams']+" -n "+geonode.nproc+" -f tregenza.cal -b tbin -m sky_glow "+geonode.filebase+"-ws.oct"
=======
                senscmd = scene['viparams']['cat']+scene['viparams']['filebase']+".rtrace | rcontrib -w  -h -I -fo -bn 146 {} -n {} -f tregenza.cal -b tbin -m sky_glow {}-ws.oct".format(simnode['radparams'], scene['viparams']['nproc'], scene['viparams']['filebase'])
>>>>>>> other
                sensrun = Popen(senscmd, shell = True, stdout=PIPE)
                
                for li, line in enumerate(sensrun.stdout):
                    decline = [float(ld) for ld in line.decode().split('\t') if ld != '\n']
                    if connode.analysismenu in ('2', '4'):
                        sensarray[li] = [179*((decline[v]*0.265)+ (decline[v+1]*0.67) + (decline[v+2]*0.065)) for v in range(0, 438, 3)]
                    elif connode.analysismenu == '3':
                        sensarray[li] = [sum(decline[v:v+3]) for v in range(0, 438, 3)]

                for l, readings in enumerate(connode['vecvals']):
                    if connode.analysismenu == '3' or (connode.cbdm_start_hour <= readings[:][0] < connode.cbdm_end_hour and readings[:][1] < connode['wd']):
<<<<<<< local
                        finalillu = [0 for x in range(geonode['reslen'])] if np == 0 else numpy.zeros((geonode['reslen']))
                        for f, fi in enumerate(finalillu):
                            finalillu[f] = numpy.sum([numpy.multiply(sensarray[f], readings[2:])]) if np == 1 else sum([a*b for a,b in zip(sensarray[f],readings[2:])])
=======
                        finalillu = [numpy.sum([numpy.multiply(sensarray[f], readings[2:])]) for f in range(geonode['reslen'])] if np == 1 else [sum([a*b for a,b in zip(sensarray[f],readings[2:])]) for f in range(geonode['reslen'])]
>>>>>>> other
                        hours += 1
                        if connode.analysismenu == '2':
                            res[findex] = numpy.sum([res[findex], [reading >= connode.dalux for reading in finalillu]], axis = 0) if np == 1 else [res[findex][k] + (0, 1)[finalillu[k] >= connode.dalux] for k in range(len(finalillu))]

                        elif connode.analysismenu == '3':
                            if np ==1:
                                if hours == 1:
                                    reswatt = numpy.zeros((len(frames), len(connode['vecvals']), geonode['reslen'])) 
                                reswatt[findex][l] = finalillu
                                [numpy.append(res[findex][i], finalillu[i]) for i in range(len(finalillu))]                                
                            else:
                                res[findex].append(finalillu)             
                        elif connode.analysismenu == '4':
<<<<<<< local
                            if np == 1:
                                target = [connode.daauto >= reading >= connode.dasupp for reading in finalillu]
                                res[findex] = numpy.sum([res[findex], target], axis = 0)
                            else:
                                res[findex] = [res[findex][k] + (0, 1)[connode.daauto >= finalillu[k] >= connode.dasupp] for k in range(len(finalillu))]
                
=======
                            res[findex] = numpy.sum([res[findex], [connode.daauto >= reading >= connode.dasupp for reading in finalillu]], axis = 0) if np == 1 else [res[findex][k] + (0, 1)[connode.daauto >= finalillu[k] >= connode.dasupp] for k in range(len(finalillu))]
                
>>>>>>> other
                if connode.analysismenu in ('2', '4'):
<<<<<<< local
                    if np == 1 and hours != 0:
                        res[findex] = res[frame]*100/hours
                    elif  np == 0 and hours != 0:
                        res[findex] = [rf*100/hours for rf in res[findex][0]]
                    with open(os.path.join(geonode.newdir, connode['resname']+"-"+str(frame)+".res"), "w") as daresfile:
=======
                    if hours != 0:
                        res[findex] = res[frame]*100/hours if np == 1 else [rf*100/hours for rf in res[findex][0]]
                    with open(os.path.join(scene['viparams']['newdir'], connode['resname']+"-"+str(frame)+".res"), "w") as daresfile:
>>>>>>> other
                        [daresfile.write("{:.2f}\n".format(r)) for r in res[findex]]
                
                if connode.analysismenu == '3':
                    res = reswatt

            if connode.analysismenu != '3' or connode.bl_label != 'LiVi CBDM':
                fi, vi = 0, 0
                for geo in vi_func.retobjs('livic'):
<<<<<<< local
                    obcalcverts, obres, weightres, sensefaces = [], [], 0, [face for face in geo.data.polygons if geo.data.materials[face.material_index].livi_sense]
                    geoarea = sum([vi_func.triarea(geo, face) for face in sensefaces])
                    if not geoarea:
                        calc_op.report({'INFO'}, geo.name+" has a livi sensor material associated with, but not assigned to any faces")
                    else: 
                        for face in sensefaces:
                            if geonode.cpoint == '1':
                                for v,vert in enumerate(face.vertices):
                                    if geo.data.vertices[vert] not in obcalcverts:
                                        weightres += res[findex][vi] 
                                        obres.append(res[findex][vi])
                                        obcalcverts.append(geo.data.vertices[vert])
                                        vi += 1
                            else:
                                weightres += vi_func.triarea(geo, face) * res[findex][fi]/geoarea
                                obres.append(res[findex][fi])
                                fi += 1
            
                        if (frame == scene.fs and not kwargs.get('genframe')) or (kwargs.get('genframe') and kwargs['genframe'] == scene.frame_start):
                            geo['oave'], geo['omax'], geo['omin'], geo['oreslist'] = {}, {}, {}, {}
    
                        geo['oave'][str(frame)] = weightres/(1, len(obcalcverts))[geonode.cpoint == '1'] 
                        geo['omax'][str(frame)] = max(obres)
                        geo['omin'][str(frame)] = min(obres)
                        geo['oreslist'][str(frame)] = obres 
                                   
        if not kwargs:
            
=======
                    lenv, lenf = len(geo['cverts']), len(geo['cfaces'])
                    sensearea = sum(geo['lisenseareas'])
                    if not sensearea:
                        calc_op.report({'INFO'}, geo.name+" has a livi sensor material associated with, but not assigned to any faces")
                    else: 
                        if geonode.cpoint == '1':
                            weightres = sum([res[findex][ri] * area for ri, area in zip(range(vi, vi+lenv), geo['lisenseareas'])])
                            obres = res[findex][vi:vi+lenv]
                            vi += lenv
                        else:
                            weightres = sum([res[findex][ri] * area for ri, area in zip(range(fi, fi+lenf), geo['lisenseareas'])])
                            obres = res[findex][fi:fi+lenf]
                            fi += lenf
                                                                   
                        if (frame == scene.fs and not kwargs.get('genframe')) or (kwargs.get('genframe') and kwargs['genframe'] == scene.frame_start):
                            geo['oave'], geo['omax'], geo['omin'], geo['oreslist'] = {}, {}, {}, {}
    
                        geo['oave'][str(frame)] = weightres/sensearea
                        geo['omax'][str(frame)] = max(obres)
                        geo['omin'][str(frame)] = min(obres)
                        geo['oreslist'][str(frame)] = obres 
                                   
        if not kwargs:           
>>>>>>> other
            resapply(calc_op, res, svres, simnode, connode, geonode)
            vi_func.vcframe('', scene, [ob for ob in scene.objects if ob.licalc] , simnode['Animation'])
        else:
            return(res[0])
   
def resapply(calc_op, res, svres, simnode, connode, geonode):
    scene = bpy.context.scene    
    if connode.analysismenu != '3' or connode.bl_label != 'LiVi CBDM':
        if np == 1:
            simnode['maxres'] = list([numpy.amax(res[i]) for i in range(scene.fs, scene.fe + 1)])
            simnode['minres'] = [numpy.amin(res[i]) for i in range(scene.fs, scene.fe + 1)]
            simnode['avres'] = [numpy.average(res[i]) for i in range(scene.fs, scene.fe + 1)]
        else:
            simnode['maxres'] = [max(res[i]) for i in range(scene.fs, scene.fe + 1)]
            simnode['minres'] = [min(res[i]) for i in range(scene.fs, scene.fe + 1)]
            simnode['avres'] = [sum(res[i])/len(res[i]) for i in range(scene.fs, scene.fe + 1)]
    
        crits = []
        dfpass = [0 for f in range(scene.fs, scene.fe + 1)]
        edfpass = [0 for f in range(scene.fs, scene.fe + 1)]
        
        for fr, frame in enumerate(range(scene.fs, scene.fe + 1)):
            scene.frame_set(frame)
            fi = 0
<<<<<<< local
            dftotarea, dfpassarea, edfpassarea, edftotarea, mcol_i, fstart, fsv, sof, eof = 0, 0, 0, 0, 0, 0, 0, 0, 0
=======
            dftotarea, dfpassarea, edfpassarea, edftotarea, mcol_i, pstart, fsv, sof, eof = 0, 0, 0, 0, 0, 0, 0, 0, 0
>>>>>>> other
            rgb, lcol_i = [], []
            if connode.bl_label != 'LiVi CBDM' or connode.analysismenu != '3':
                for i in range(len(res[fr])):
                    h = 0.75*(1-(res[fr][i]-min(simnode['minres']))/(max(simnode['maxres']) + 0.01 - min(simnode['minres'])))
                    rgb.append(colorsys.hsv_to_rgb(h, 1.0, 1.0))
        
            if bpy.context.active_object and bpy.context.active_object.hide == 'False':
                bpy.ops.object.mode_set()
        
            for geo in vi_func.retobjs('livic'):
                bpy.ops.object.select_all(action = 'DESELECT')
                scene.objects.active = None
                geoareas = geo['lisenseareas']
                geoarea = sum(geoareas)
                lenpoints = len(geo['cfaces']) if geonode.cpoint == '0' else len(geo['cverts'])
                geofaces = [face for face in geo.data.polygons if geo.data.materials[face.material_index].livi_sense]
                geos = [geo.data.polygons[fi] for fi in geo['cfaces']] if geonode.cpoint == '0' else [geo.data.vertices[vi] for vi in geo['cverts']]

                if geo.get('wattres'):
                    del geo['wattres']
                
<<<<<<< local
                fend = fstart + len(geofaces)
                passarea = 0
=======
                pend, passarea = pstart + lenpoints, 0
>>>>>>> other
                vi_func.selobj(scene, geo)
                bpy.ops.mesh.vertex_color_add()
                geo.data.vertex_colors[-1].name = str(frame)
                vertexColour = geo.data.vertex_colors[str(frame)]
                mat = [matslot.material for matslot in geo.material_slots if matslot.material.livi_sense][0]
                mcol_i = len(tuple(set(lcol_i)))

                for face in geofaces:
                    if geonode.cpoint == '1':
                        cvtup = tuple(geo['cverts'])
                        for loop_index in face.loop_indices:
                            v = geo.data.loops[loop_index].vertex_index
                            if v in cvtup:
                                col_i = cvtup.index(v)
                            lcol_i.append(col_i)
                            vertexColour.data[loop_index].color = rgb[col_i+mcol_i]
        
                    if geonode.cpoint == '0':
                        for loop_index in face.loop_indices:
                            vertexColour.data[loop_index].color = rgb[fi]
                        fi += 1

                if connode.bl_label == 'LiVi Compliance':
                    if connode.analysismenu == '1':
                        bpy.ops.mesh.vertex_color_add()
                        geo.data.vertex_colors[-1].name = '{}sv'.format(frame)
                        vertexColour = geo.data.vertex_colors['{}sv'.format(frame)]
                        for face in geofaces:
                            if geonode.cpoint == '1':
                                cvtup = tuple(geo['cverts'])
                                for loop_index in face.loop_indices:
                                    v = geo.data.loops[loop_index].vertex_index
                                    if v in cvtup:
                                        col_i = cvtup.index(v)
                                    lcol_i.append(col_i)
                                    vertexColour.data[loop_index].color = rgb[col_i+mcol_i]

                            elif geonode.cpoint == '0':
                                for loop_index in face.loop_indices:
                                    vertexColour.data[loop_index].color = (0, 1, 0) if svres[frame][fsv] > 0 else (1, 0, 0)
                                fsv += 1

                    if fr == 0:
<<<<<<< local
                        crit, ecrit = [], []
                        comps, ecomps =  [[[] * fra for fra in range(scene.fs, scene.fe + 1)] for x in range(2)]

=======
                        comps, ecomps =  [[[] * fra for fra in range(scene.fs, scene.fe + 1)] for x in range(2)]
>>>>>>> other
                        if connode.analysismenu == '0':
                            if connode.bambuildmenu in ('0', '5'):
                                if not mat.gl_roof:
<<<<<<< local
                                    crit.append(['Percent', 80, 'DF', 2, '1'])
                                    crit.append(['Ratio', 100, 'Uni', 0.4, '0.5'])
                                    crit.append(['Min', 100, 'PDF', 0.8, '0.5'])
                                    crit.append(['Percent', 80, 'Skyview', 1, '0.75'])

                                    if connode.buildstorey == '0':
                                        ecrit.append(['Percent', 80, 'DF', 4, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 1.6, '0.75'])

                                    elif connode.buildstorey == '1':
                                        ecrit.append(['Percent', 80, 'DF', 3, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 1.2, '0.75'])
=======
                                    crit = [['Percent', 80, 'DF', 2, '1'], ['Ratio', 100, 'Uni', 0.4, '0.5'], ['Min', 100, 'PDF', 0.8, '0.5'], ['Percent', 80, 'Skyview', 1, '0.75']]
                                    ecrit = [['Percent', 80, 'DF', 4, '1'], ['Min', 100, 'PDF', 1.6, '0.75']] if connode.buildstorey == '0' else [['Percent', 80, 'DF', 3, '1'], ['Min', 100, 'PDF', 1.2, '0.75']] 
>>>>>>> other
                                else:
<<<<<<< local
                                    crit.append(['Percent', 80, 'DF', 2, '1'])
                                    crit.append(['Ratio', 100, 'Uni', 0.7, '0.5'])
                                    crit.append(['Min', 100, 'PDF', 1.4, '0.5'])
                                    crit.append(['Percent', 100, 'Skyview', 1, '0.75'])

                                    if connode.buildstorey == '0':
                                        ecrit.append(['Percent', 80, 'DF', 4, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 2.8, '0.75'])

                                    elif connode.buildstorey == '1':
                                        ecrit.append(['Percent', 80, 'DF', 3, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 2.1, '0.75'])
=======
                                    crit = [['Percent', 80, 'DF', 2, '1'], ['Ratio', 100, 'Uni', 0.7, '0.5'], ['Min', 100, 'PDF', 1.4, '0.5'], ['Percent', 100, 'Skyview', 1, '0.75']]
                                    ecrit = [['Percent', 80, 'DF', 4, '1'], ['Min', 100, 'PDF', 2.8, '0.75']] if connode.buildstorey == '0' else [['Percent', 80, 'DF', 3, '1'], ['Min', 100, 'PDF', 2.1, '0.75']]
>>>>>>> other

                            elif connode.bambuildmenu == '1':
                                if not mat.gl_roof:
<<<<<<< local
                                    crit.append(['Percent', 80, 'DF', 2, '1'])
#                                    crit.append(['Percent', 80, 'DF', 2, '1'])
                                    crit.append(['Ratio', 100, 'Uni', 0.4, '0.5'])
                                    crit.append(['Min', 100, 'PDF', 0.8, '0.5'])
                                    crit.append(['Percent', 80, 'Skyview', 1, '0.75'])

                                    if connode.buildstorey == '0':
                                        ecrit.append(['Percent', 80, 'DF', 4, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 1.6, '0.75'])

                                    elif connode.buildstorey == '1':
                                        ecrit.append(['Percent', 80, 'DF', 3, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 1.2, '0.75'])
=======
                                    crit = [['Percent', 80, 'DF', 2, '1'], ['Ratio', 100, 'Uni', 0.4, '0.5'], ['Min', 100, 'PDF', 0.8, '0.5'], ['Percent', 80, 'Skyview', 1, '0.75']]
                                    ecrit = [['Percent', 80, 'DF', 4, '1'], ['Min', 100, 'PDF', 1.6, '0.75']] if connode.buildstorey == '0' else [['Percent', 80, 'DF', 3, '1'], ['Min', 100, 'PDF', 1.2, '0.75']]
>>>>>>> other
                                else:
<<<<<<< local
                                    crit.append(['Percent', 80, 'DF', 2, '1'])
#                                    crit.append(['Percent', 80, 'DF', 2, '1'])
                                    crit.append(['Ratio', 100, 'Uni', 0.7, '0.5'])
                                    crit.append(['Min', 100, 'PDF', 1.4, '0.5'])
                                    crit.append(['Percent', 100, 'Skyview', 1, '0.75'])

                                    if connode.buildstorey == '0':
                                        ecrit.append(['Percent', 80, 'DF', 4, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 2.8, '0.75'])

                                    elif connode.buildstorey == '1':
                                        ecrit.append(['Percent', 80, 'DF', 3, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 2.1, '0.75'])
=======
                                    crit = [['Percent', 80, 'DF', 2, '1'], ['Ratio', 100, 'Uni', 0.7, '0.5'], ['Min', 100, 'PDF', 1.4, '0.5'], ['Percent', 100, 'Skyview', 1, '0.75']]
                                    ecrit= [['Percent', 80, 'DF', 4, '1'], ['Min', 100, 'PDF', 2.8, '0.75']] if connode.buildstorey == '0' else [['Percent', 80, 'DF', 3, '1'], ['Min', 100, 'PDF', 2.1, '0.75']]
>>>>>>> other

                            elif connode.bambuildmenu == '2':
                                crit = [['Percent', 80, 'DF', 2, '1']] if mat.hspacemenu == '0' else [['Percent', 80, 'DF', 3, '2']]
                                ecrit = [['Percent', 80, 'DF', 4, '1'], ['Min', 100, 'PDF', 1.6, '0.75']] if connode.buildstorey == '0' else [['Min', 100, 'PDF', 1.6, '0.75'], ['Min', 100, 'PDF', 1.2, '0.75']]
               
                            elif connode.bambuildmenu == '3':
                                if mat.brspacemenu == '0':
                                    crit = [['Percent', 80, 'DF', 2, '1'], ['Percent', 100, 'Skyview', 1, '0.75']]
                                    ecrit = [['Percent', 80, 'DF', 4, '1'], ['Min', 100, 'PDF', 1.6, '0.75']] if connode.buildstorey == '0' else [['Percent', 80, 'DF', 3, '1'], ['Min', 100, 'PDF', 1.2, '0.75']]

<<<<<<< local
                                if connode.buildstorey == '0':
                                    ecrit.append(['Percent', 80, 'DF', 4, '1'])
                                    ecrit.append(['Min', 100, 'PDF', 1.6, '0.75'])
=======
                                elif mat.brspacemenu == '1':
                                    crit = [['Percent', 80, 'DF', 1.5, '1'], ['Percent', 100, 'Skyview', 1, '0.75']]
                                    ecrit = [['Percent', 80, 'DF', 4, '1'], ['Min', 100, 'PDF', 1.6, '0.75']] if connode.buildstorey == '0' else [['Percent', 80, 'DF', 3, '1'], ['Min', 100, 'PDF', 1.2, '0.75']]
>>>>>>> other

<<<<<<< local
                                elif connode.buildstorey == '1':
                                    ecrit.append(['Percent', 80, 'DF', 3, '1'])
                                    ecrit.append(['Min', 100, 'PDF', 1.2, '0.75'])

                            elif connode.bambuildmenu == '3':
                                if mat.rspacemenu == '0':
                                    crit.append(['Percent', 80, 'DF', 2, '1'])
                                    crit.append(['Percent', 100, 'Skyview', 1, '0.75'])

                                    if connode.buildstorey == '0':
                                        ecrit.append(['Percent', 80, 'DF', 4, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 1.6, '0.75'])

                                    elif connode.buildstorey == '1':
                                        ecrit.append(['Percent', 80, 'DF', 3, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 1.2, '0.75'])

                                elif mat.rspacemenu == '1':
                                    crit.append(['Percent', 80, 'DF', 1.5, '1'])
                                    crit.append(['Percent', 100, 'Skyview', 1, '0.75'])

                                    if connode.buildstorey == '0':
                                        ecrit.append(['Percent', 80, 'DF', 4, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 1.6, '0.75'])

                                    elif connode.buildstorey == '1':
                                        ecrit.append(['Percent', 80, 'DF', 3, '1'])
                                        ecrit.append(['Min', 100, 'PDF', 1.2, '0.75'])

                                elif mat.rspacemenu == '2':
=======
                                elif mat.brspacemenu == '2':
>>>>>>> other
                                    if not mat.gl_roof:
<<<<<<< local
                                        crit.append(['Percent', 80, 'DF', 2, '1'])
                                        crit.append(['Ratio', 100, 'Uni', 0.4, '0.5'])
                                        crit.append(['Min', 100, 'PDF', 0.8, '0.5'])
                                        crit.append(['Percent', 80, 'Skyview', 1, '0.75'])

                                        if connode.buildstorey == '0':
                                            ecrit.append(['Percent', 80, 'DF', 4, '1'])
                                            ecrit.append(['Min', 100, 'PDF', 1.6, '0.75'])

                                        elif connode.buildstorey == '1':
                                            ecrit.append(['Percent', 80, 'DF', 3, '1'])
                                            ecrit.append(['Min', 100, 'PDF', 1.2, '0.75'])
=======
                                        crit = [['Percent', 80, 'DF', 2, '1'], ['Ratio', 100, 'Uni', 0.4, '0.5'], ['Min', 100, 'PDF', 0.8, '0.5'], ['Percent', 80, 'Skyview', 1, '0.75']]
                                        ecrit = [['Percent', 80, 'DF', 4, '1'], ['Min', 100, 'PDF', 1.6, '0.75']] if connode.buildstorey == '0' else [['Percent', 80, 'DF', 3, '1'], ['Min', 100, 'PDF', 1.2, '0.75']]
>>>>>>> other
                                    else:
<<<<<<< local
                                        crit.append(['Percent', 80, 'DF', 2, '1'])
                                        crit.append(['Ratio', 100, 'Uni', 0.7, '0.5'])
                                        crit.append(['Min', 100, 'PDF', 1.4, '0.5'])
                                        crit.append(['Percent', 100, 'Skyview', 1, '0.75'])

                                        if connode.buildstorey == '0':
                                            ecrit.append(['Percent', 80, 'DF', 4, '1'])
                                            ecrit.append(['Min', 100, 'PDF', 2.8, '0.75'])

                                        elif connode.buildstorey == '1':
                                            ecrit.append(['Percent', 80, 'DF', 3, '1'])
                                            ecrit.append(['Min', 100, 'PDF', 2.1, '0.75'])
=======
                                        crit = [['Percent', 80, 'DF', 2, '1'], ['Ratio', 100, 'Uni', 0.7, '0.5'],['Min', 100, 'PDF', 1.4, '0.5'], ['Percent', 100, 'Skyview', 1, '0.75']] 
                                        ecrit = [['Percent', 80, 'DF', 4, '1'], ['Min', 100, 'PDF', 2.8, '0.75']] if connode.buildstorey == '0' else [['Percent', 80, 'DF', 3, '1'], ['Min', 100, 'PDF', 2.1, '0.75']]
>>>>>>> other

                            elif connode.bambuildmenu == '4':
                                if mat.respacemenu == '0':
                                    crit = [['Percent', 35, 'PDF', 2, '1']]
                                    ecrit = [['Percent', 50, 'PDF', 2, '1']]

                                elif mat.respacemenu == '1':
                                    if not mat.gl_roof:
<<<<<<< local
                                        crit.append(['Percent', 80, 'DF', 2, '1'])
                                        crit.append(['Ratio', 100, 'Uni', 0.4, '0.5'])
                                        crit.append(['Min', 100, 'PDF', 0.8, '0.5'])
                                        crit.append(['Percent', 80, 'Skyview', 1, '0.75'])

                                        if connode.buildstorey == '0':
                                            ecrit.append(['Percent', 80, 'DF', 4, '1'])
                                            ecrit.append(['Min', 100, 'PDF', 1.6, '0.75'])

                                        elif connode.buildstorey == '1':
                                            ecrit.append(['Percent', 80, 'DF', 3, '1'])
                                            ecrit.append(['Min', 100, 'PDF', 1.2, '0.75'])
=======
                                        crit = [['Percent', 80, 'DF', 2, '1'], ['Ratio', 100, 'Uni', 0.4, '0.5'], ['Min', 100, 'PDF', 0.8, '0.5'], ['Percent', 80, 'Skyview', 1, '0.75']] 
                                        ecrit = [['Percent', 80, 'DF', 4, '1'], ['Min', 100, 'PDF', 1.6, '0.75']] if connode.buildstorey == '0' else [['Percent', 80, 'DF', 3, '1'], ['Min', 100, 'PDF', 1.2, '0.75']]
           
>>>>>>> other
                                    else:
<<<<<<< local
                                        crit.append(['Percent', 80, 'DF', 2, '1'])
                                        crit.append(['Ratio', 100, 'Uni', 0.7, '0.5'])
                                        crit.append(['Min', 100, 'PDF', 1.4, '0.5'])
                                        crit.append(['Percent', 100, 'Skyview', 1, '0.75'])

                                        if connode.buildstorey == '0':
                                            ecrit.append(['Percent', 80, 'DF', 4, '1'])
                                            ecrit.append(['Min', 100, 'PDF', 2.8, '0.75'])

                                        elif connode.buildstorey == '1':
                                            ecrit.append(['Percent', 80, 'DF', 3, '1'])
                                            ecrit.append(['Min', 100, 'PDF', 2.1, '0.75'])
=======
                                        crit = [['Percent', 80, 'DF', 2, '1'], ['Ratio', 100, 'Uni', 0.7, '0.5'], ['Min', 100, 'PDF', 1.4, '0.5'], ['Percent', 100, 'Skyview', 1, '0.75']]
                                        ecrit = [['Percent', 80, 'DF', 4, '1'], ['Min', 100, 'PDF', 2.8, '0.75']] if connode.buildstorey == '0' else [['Percent', 80, 'DF', 3, '1'],['Min', 100, 'PDF', 2.1, '0.75']] 
>>>>>>> other

                        elif connode.analysismenu == '1':
                            crit = [['Average', 100, 'DF', 2, '1'], ['Percent', 80, 'Skyview', 1, '0.75']] if mat.crspacemenu == '0' else [['Average', 100, 'DF', 1.5, '1'], ['Percent', 80, 'Skyview', 1, '0.75']]
                            ecrit = []
                        elif connode.analysismenu == '2':
                            crit = [['Percent', 75, 'FC', 108, '1'], ['Percent', 75, 'FC', 5400, '1'], ['Percent', 90, 'FC', 108, '1'], ['Percent', 90, 'FC', 5400, '1']]
                            ecrit = []
                    for c in crit:
                        if c[0] == 'Percent':
                            if c[2] == 'DF':
                                dfpass[frame] = 1
                                dfpassarea = dfpassarea + geoarea if sum(res[frame][pstart:pend])/(pend - pstart) > c[3] else dfpassarea
                                comps[frame].append((0, 1)[sum(res[frame][pstart:pend])/(pend - pstart) > c[3]])
                                comps[frame].append(sum(res[frame][pstart:pend])/(pend - pstart))
                                dftotarea += geoarea
                                
                            if c[2] == 'PDF':
                                dfpass[frame] = 1
                                dfpassarea = sum([area for p, area in enumerate(geoareas) if res[frame][p + pstart] > c[3]])
                                comps[frame].append((0, 1)[dfpassarea > c[1]*geoarea/100])
                                comps[frame].append(100*dfpassarea/geoarea)
                                dftotarea += geoarea
<<<<<<< local
                                
                            if c[2] == 'PDF':
                                dfpass[frame] = 1
                                for fa, face in enumerate(geofaces):
                                    if res[frame][fa + fstart] > c[3]:
                                        dfpassarea += vi_func.triarea(geo, face)
                                if dfpassarea > c[1]*geoarea/100:
                                    comps[frame].append(1)
                                else:
                                    comps[frame].append(0)
                                comps[frame].append(100*dfpassarea/geoarea)
                                dftotarea += geoarea
                                    
#                                if sum(res[frame][fstart:fend])/(fend - fstart) > c[3]:
#                                    dfpassarea += geoarea
#                                    comps[frame].append(1)
#                                else:
#                                    comps[frame].append(0)
#                                comps[frame].append(sum(res[frame][fstart:fend])/(fend - fstart))
#                                dftotarea += geoarea

=======

>>>>>>> other
                            elif c[2] == 'Skyview':
                                passarea = sum([area for p, area in enumerate(geoareas) if svres[frame][p + pstart] > 0])
                                comps[frame].append((0, 1)[passarea >= c[1]*geoarea/100])
                                comps[frame].append(100*passarea/geoarea)
                                passarea = 0

                        elif c[0] == 'Min':
                            comps[frame].append((0, 1)[min(res[frame][pstart:pend]) > c[3]])
                            comps[frame].append(min(res[frame][pstart:pend]))

                        elif c[0] == 'Ratio':
<<<<<<< local
                            if min(res[frame][fstart:fend])/(sum(res[frame][fstart:fend])/(fend - fstart)) >= c[3]:
                                comps[frame].append(1)
                            else:
                                comps[frame].append(0)
                            comps[frame].append(min(res[frame][fstart:fend])/(sum(res[frame])/(fend - fstart)))
=======
                            comps[frame].append((0, 1)[min(res[frame][pstart:pend])/(sum(res[frame][pstart:pend])/(pend - pstart)) >= c[3]])
                            comps[frame].append(min(res[frame][pstart:pend])/(sum(res[frame])/(pend - pstart)))
>>>>>>> other

                        elif c[0] == 'Average':
                            comps[frame].append((0, 1)[sum([area * res[frame][p + pstart] for p, area in enumerate(geoareas)])/geoarea > c[3]])
                            comps[frame].append(sum([area * res[frame][p + pstart] for p, area in enumerate(geoareas)])/geoarea)

                    for e in ecrit:
                        if e[0] == 'Percent':
                            if e[2] == 'DF':
<<<<<<< local
                                edfpass[frame] = 1
                                if sum(res[frame][fstart:fend])/(fend - fstart) > e[3]:
                                    edfpassarea += geoarea
                                ecomps[frame].append((0, 1)[sum(res[frame][fstart:fend])/(fend - fstart) > e[3]])
                                ecomps[frame].append(sum(res[frame][fstart:fend])/(fend - fstart))
=======
                                edfpass[frame] = [1, (0, 1)[sum(res[frame][pstart:pend])/(pend - pstart) > e[3]], sum(res[frame][pstart:pend])/(pend - pstart)]
                                edfpassarea = edfpassarea + geoarea if sum(res[frame][pstart:pend])/(pend - pstart) > e[3] else edfpassarea
                                ecomps[frame].append((0, 1)[sum(res[frame][pstart:pend])/(pend - pstart) > e[3]])
                                ecomps[frame].append(sum(res[frame][pstart:pend])/(pend - pstart))
                                edftotarea += geoarea
                                
                            if e[2] == 'PDF':
                                edfpass[frame] = 1
                                edfpassarea = sum([vi_func.facearea(geo, face) for fa, face in enumerate(geofaces) if res[frame][fa + pstart] > e[3]])      
                                ecomps[frame].append((0, 1)[dfpassarea > e[1]*geoarea/100])
                                ecomps[frame].append(100*edfpassarea/geoarea)
>>>>>>> other
                                edftotarea += geoarea
<<<<<<< local
                                
                            if e[2] == 'PDF':
                                edfpass[frame] = 1
                                for fa, face in enumerate(geofaces):
                                    if res[frame][fa + fstart] > e[3]:
                                        edfpassarea += vi_func.triarea(geo, face)
                                if dfpassarea > e[1]*geoarea/100:
                                    ecomps[frame].append(1)
                                else:
                                    ecomps[frame].append(0)
                                ecomps[frame].append(100*edfpassarea/geoarea)
                                edftotarea += geoarea

=======

>>>>>>> other
                            elif e[2] == 'Skyview':
                                passarea = sum([vi_func.facearea(geo, face) for fa, face in enumerate(geofaces) if svres[frame][fa] > 0])
                                ecomps[frame].append((0, 1)[passarea >= e[1] * geoarea/100])
                                ecomps[frame].append(100*passarea/geoarea)
                                passarea = 0

                        elif e[0] == 'Min':
                            ecomps[frame].append((0, 1)[min(res[frame][pstart:pend]) > e[3]])
                            ecomps[frame].append(min(res[frame][pstart:pend]))

                        elif e[0] == 'Ratio':
                            ecomps[frame].append((0, 1)[min(res[frame][pstart:pend])/(sum(res[frame][pstart:pend])/(pend - pstart)) >= e[3]])
                            ecomps[frame].append(min(res[frame][pstart:pend])/(sum(res[frame][pstart:pend])/(pend - pstart)))

                        elif e[0] == 'Average':
                            ecomps[frame].append((0, 1)[sum(res[frame][pstart:pend])/(pend - pstart) > e[3]])
                            ecomps[frame].append(sum(res[frame][pstart:pend])/(pend - pstart))

                    geo['crit'], geo['ecrit'], geo['comps'], geo['ecomps'] = [[c[0], str(c[1]), c[2], str(c[3]), c[4]] for c in crit[:]], [[c[0], str(c[1]), c[2], str(c[3]), c[4]] for c in ecrit[:]], comps, ecomps
                    crits.append(geo['crit'])
                    pstart = pend
    
        if connode.bl_label == 'LiVi Compliance': 
            if dfpass[frame] == 1:
<<<<<<< local
                dfpass[frame] = 2 if dfpassarea/dftotarea >= (0.8, 0.35)[connode.analysismenu == '0' and connode.bambuildtype == '4'] else dfpass[frame]
            if edfpass[frame] == 1:
                edfpass[frame] = 2 if edfpassarea/edftotarea >= (0.8, 0.5)[connode.analysismenu == '0' and connode.bambuildtype == '4'] else edfpass[frame]
            scene['crits'] = crits
            scene['dfpass'] = dfpass
=======
                dfpass[frame] = 2 if dfpassarea/dftotarea >= (0.8, 0.35)[connode.analysismenu == '0' and connode.bambuildtype == '4'] else dfpass[frame]
            if edfpass[frame] == 1:
                edfpass[frame] = 2 if edfpassarea/edftotarea >= (0.8, 0.5)[connode.analysismenu == '0' and connode.bambuildtype == '4'] else edfpass[frame]
            scene['crits'], scene['dfpass'] = crits, dfpass
>>>>>>> other
        simnode.outputs['Data out'].hide = True
    else:
        for fr, frame in enumerate(range(scene.fs, scene.fe + 1)):
            scene.frame_set(frame)
            sof, sov = 0, 0
            for geo in vi_func.retobjs('livic'):
                bpy.ops.object.select_all(action = 'DESELECT')
                eof, eov, hours, scene.objects.active = sof + len(geo['cfaces']), sov + len(geo['cverts']), len(res[0]), None
                geoarea = sum(geo['lisenseareas'])
                geofaces = [face for face in geo.data.polygons if geo.data.materials[face.material_index].livi_sense]
                geo['wattres'] = {str(frame):[0 for x in range(len(res[0]))]}
                for i in range(hours):
                    if geonode.cpoint == '0':
                        geo['wattres'][str(frame)][i] = sum([res[fr][i][sof:eof][j] * geo['lisenseareas'][j] for j in range(sof, eof)])
                    else:
                        geo['wattres'][str(frame)][i] = sum([res[fr][i][sov:eov][j] * geo['lisenseareas'][j] for j in range(sov, eov)])
                sov, sof = eov, eof

        simnode.outputs['Data out'].hide = False
            
    calc_op.report({'INFO'}, "Calculation is finished.")
    bpy.ops.wm.save_mainfile(check_existing = False)
<<<<<<< local

def li_glare(calc_op, simnode, connode, geonode):
    scene = bpy.context.scene
    cam = scene.camera
    if cam:
#        num = (("-ab", 2, 3, 5), ("-ad", 512, 2048, 4096), ("-ar", 128, 512, 1024), ("-as", 256, 1024, 2048), ("-aa", 0.3, 0.2, 0.18), ("-dj", 0, 0.7, 1), ("-ds", 0, 0.5, 0.15), ("-dr", 1, 2, 3), ("-ss", 0, 2, 5), ("-st", 1, 0.75, 0.1), ("-lw", 0.05, 0.001, 0.0002))
#        params = (" {0[0]} {1[0]} {0[1]} {1[1]} {0[2]} {1[2]} {0[3]} {1[3]} {0[4]} {1[4]} {0[5]} {1[5]} {0[6]} {1[6]} {0[7]} {1[7]} {0[8]} {1[8]} {0[9]} {1[9]} {0[10]} {1[10]} ".format([n[0] for n in num], [n[int(simnode.simacc)+1] for n in num]))
        
        for frame in range(scene.fs, scene.fe + 1):
            time = datetime.datetime(2014, 1, 1, connode.shour, 0) + datetime.timedelta(connode.sdoy - 1) if connode.animmenu == '0' else \
            datetime.datetime(2014, 1, 1, int(connode.shour), int(60*(connode.shour - int(connode.shour)))) + datetime.timedelta(connode.sdoy - 1) + datetime.timedelta(hours = int(connode.interval*(frame-scene.frame_start)), seconds = int(60*(connode.interval*(frame-scene.frame_start) - int(connode.interval*(frame-scene.frame_start)))))
            glarecmd = "rpict -w -vth -vh 180 -vv 180 -x 800 -y 800 -vd {0[0][2]} {0[1][2]} {0[2][2]} -vp {1[0]} {1[1]} {1[2]} {2} {3}-{5}.oct | evalglare -c {4}.hdr".format(-1*cam.matrix_world, cam.location, simnode['radparams'], geonode.filebase, os.path.join(geonode.newdir, 'glare'+str(frame)), frame)               
            glarerun = Popen(glarecmd, shell = True, stdout = PIPE)
            glaretf = open(geonode.filebase+".glare", "w")
            for line in glarerun.stdout:
                if line.decode().split(",")[0] == 'dgp':
                    glaretext = line.decode().replace(',', ' ').replace("#INF", "").split(' ')                    
                    glaretf.write("{0:0>2d}/{1:0>2d} {2:0>2d}:{3:0>2d}\ndgp: {4:.3f}\ndgi: {5:.3f}\nugr: {6:.3f}\nvcp: {7:.3f}\ncgi: {8:.3f}\nLveil: {9:.3f}\n".format(time.day, time.month, time.hour, time.minute, *[float(x) for x in glaretext[6:12]]))
                    glaretf.close()
            subprocess.call("pcond -u 300 {0}.hdr > {0}.temphdr".format(os.path.join(geonode.newdir, 'glare'+str(frame))), shell=True)
            subprocess.call("{0} {1}.glare | psign -h 32 -cb 0 0 0 -cf 40 40 40 | pcompos {3}.temphdr 0 0 - 800 550 > {3}.hdr" .format(geonode.cat, geonode.filebase, frame, os.path.join(geonode.newdir, 'glare'+str(frame))), shell=True)
            subprocess.call("{} {}.temphdr".format(geonode.rm, os.path.join(geonode.newdir, 'glare'+str(frame))), shell=True)                    
            if  'glare{}.hdr'.format(frame) in bpy.data.images:
                bpy.data.images['glare{}.hdr'.format(frame)].reload()
            else:
                bpy.data.images.load(os.path.join(geonode.newdir, 'glare{}.hdr'.format(frame)))
                
    else:
        calc_op.report({'ERROR'}, "There is no camera in the scene. Create one for glare analysis")=======
>>>>>>> other
