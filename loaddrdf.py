import drdf
import matplotlib.pyplot as plt
import numpy as np

def load_drdf(fname):
  reader = drdf.DRDF()
  reader.read(fname)
  events = []
  for run in reader.runs:#fa il loop sulle keys dei dict (in questo caso è solo una chiave)
    for event in reader.runs[run]:#fa il loop sulle chiavi di reader.runs[run]
      hits_map = dict()
      for cam, img in reader.runs[run][event].items():
        # print(cam, img)
        amplitude = img.pixels[:, :, 0]
        # print(amplitude[0][0])
        time = img.pixels[:, :, 1]
        hits_map[cam] = amplitude
      events.append((event, hits_map))
  return events

file = load_drdf("response4.drdf")

# ISTOGRAMMA CON NUMERO DI EVENTI PER OGNI RUN --------------------- ma è il numero di eventi (cioè di fotoni prodotti o di camere colpite) oppure è il numero dell'evento (cioè evento numero 1, numero 2 ecc.)? 
nr_events = []
for i in range(len(file)):
  nr_events.append(file[i][0])
#print(nr_events)

# plt.hist(nr_events, 50)
# plt.xlabel("# of events")
# plt.ylabel("occurences")
# plt.title("# of events in all the runs")
# plt.show()
# ---------------------------------------------------------------------------------


# 1D HISTO: NUMERO DI HIT IN UNA UNICA CAMERA CAM_NB_X0 per ogni evento:-----------------------
pixels_hit_cam1 = []
for i in range(len(file)):
    event_i = file[i][1]# così sto considerando file, nell'evento i esimo, la parte di hits_map (che  un dict)
    event_i_list = list(file[i][1].values())#rendo il dictionary hits_map una lista: ho tutti i valori di amplitude come matrice
    event_i_cam1 = event_i_list[0]#qui ho tutti gli hits in cam1
    for j in range(len(event_i_cam1)):
        pixels_hit_cam1.append(event_i_cam1[j])
# print(pixels_hit_cam1, "********************")

# plt.hist(pixels_hit_cam1, 10, (0.1,2))
# plt.xlabel("# of hits")
# plt.ylabel("occurences")
# plt.title("# of hits on cam 1")
# plt.show()
# # ----------------------------------------------------------------------------------


# 2D HISTO: NUMERO DI HIT NELLA PRIMA CAMERA CAM_NB_X0 per ogni evento COME MATRICE:-----------------------
pixels_hit_cam1 = []
cam1_all = np.zeros((32,32))
#print(cam1_all)
for i in range(len(file)):
    event_i = file[i][1]# così sto considerando file, nell'evento i esimo, la parte di hits_map (che  un dict)
    event_i_cam1 = event_i['CAM_NB_X0']#qui ho amplitude per cam1, cioè tutti gli hits di cam1 ma in una matrice
    cam1_all = np.add(cam1_all, event_i_cam1)
print(cam1_all)

plt.imshow(cam1_all, interpolation='none')
plt.colorbar()
plt.title("total events on CAM_NB_X0")
plt.show()
# ----------------------------------------------------------------------------------------------------------

# 2D HISTO: NUMERO DI HIT PER UN SINGOLO EVENTO (L'EVENTO NR 4594), PER OGNI CAMERA. 
# Avevo visto che per questo evento nelle camere NN_Y1, NN_Y2 ci può essere una produzione di un fotone dentro-------
for cam in event_i:
    event_4594_cam = file[151][1][cam]
    plt.imshow(event_4594_cam, interpolation = 'none')
    plt.title(f"event 4594 in {cam}")
    plt.colorbar()
    plt.show()
# --------------------------------------------------------------------------------------------------------------------


# 2D HISTO: NUMERO DI HIT PER OGNI CAMERA per ogni evento COME MATRICE:---------------------------------------
for cam in event_i:
    cam_j_all = np.zeros((32,32))
    for i in range(len(file)):
        event_i = file[i][1]# così sto considerando file, nell'evento i esimo, la parte di hits_map (che  un dict)
        if np.any(event_i[cam] != 0.):
            event_i_cam_j = event_i[cam]#qui ho amplitude per cam1, cioè tutti gli hits di cam j esima ma in una matrice
            plt.imshow(event_i_cam_j, interpolation='none')
            plt.colorbar()
            plt.title(f"event {file[i][0]} on {cam}")
            plt.show()
            cam_j_all = np.add(cam_j_all, event_i_cam_j)#PROBLEMA!!! cam j all rimane riempita con gli eventi della camera prima 
        #print(cam1_all)
    plt.imshow(cam_j_all, interpolation='none')
    plt.colorbar()
    plt.title(f"total events on {cam}")
    plt.show()
# --------------------------------------------------------------------------------------------------

# SCATTER PLOT: 
cam_list = []
counts = 0
# for i in range(len(file)):
all_cam_list = []
for cam in event_i:
    event_i = file[i][1]
    cam_list.append(cam)
    if np.any(event_i[cam] != 0.):
        counts += 1
        sum_cam_all = sum(map(sum, event_i[cam]))
        print(sum_cam_all)
        all_cam_list.append(sum_cam_all) 
print(counts)
print(len(all_cam_list)) 
plt.scatter(all_cam_list, cam_list)
plt.title(f"plot - # photons of event {file[i][0]} for each camera")
plt.show()
