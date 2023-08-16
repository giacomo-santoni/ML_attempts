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


# 2D HISTO: NUMERO DI HIT NELLA PRIMA CAMERA CAM_NB_X0 per ogni evento COME MATRICE:-----------------------
def Pixels1Cam():
  cam1_all = np.zeros((32,32))
  for i in range(len(file)):
      event_i = file[i][1]# così sto considerando file, nell'evento i esimo, la parte di hits_map (che  un dict)
      if np.any(event_i['CAM_NW_X4_Y1'] != 0.):
          event_i_cam1 = event_i['CAM_NW_X4_Y1']#qui ho amplitude per cam1, cioè tutti gli hits di cam1 ma in una matrice
          #print(file[i][0], " ", event_i_cam1)
          plt.imshow(event_i_cam1, interpolation='none')
          plt.colorbar()
          plt.title(f"event {file[i][0]} on CAM_NW_X4_Y1")
          plt.show()
          cam1_all = np.add(cam1_all, event_i_cam1)
  return cam1_all

def twodimHistoPixels1Cam():
    cam1_all = Pixels1Cam()
    plt.imshow(cam1_all, interpolation='none')
    plt.colorbar()
    plt.title("total events on CAM_NW_X4_Y1")
    plt.show()


# Pixels1Cam()
# twodimHistoPixels1Cam()
# ----------------------------------------------------------------------------------------------------------

# 2D HISTO: NUMERO DI HIT PER UN SINGOLO EVENTO (L'EVENTO NR 4594), PER OGNI CAMERA. 
# Avevo visto che per questo evento nelle camere NN_Y1, NN_Y2 ci può essere una produzione di un fotone dentro-------
# for cam in event_i:
#     event_4594_cam = file[151][1][cam]
#     plt.imshow(event_4594_cam, interpolation = 'none')
#     plt.title(f"event 4594 in {cam}")
#     plt.colorbar()
#     plt.show()
# --------------------------------------------------------------------------------------------------------------------


# 2D HISTO: NUMERO DI HIT PER OGNI CAMERA per ogni evento COME MATRICE:---------------------------------------
# for cam in event_i:
#     cam_j_all = np.zeros((32,32))
#     for i in range(len(file)):
#         event_i = file[i][1]# così sto considerando file, nell'evento i esimo, la parte di hits_map (che  un dict)
#         if np.any(event_i[cam] != 0.):
#             event_i_cam_j = event_i[cam]#qui ho amplitude per cam1, cioè tutti gli hits di cam j esima ma in una matrice
#             plt.imshow(event_i_cam_j, interpolation='none')
#             plt.colorbar()
#             plt.title(f"event {file[i][0]} on {cam}")
#             plt.show()
#             cam_j_all = np.add(cam_j_all, event_i_cam_j)#PROBLEMA!!! cam j all rimane riempita con gli eventi della camera prima 
#         #print(cam1_all)
#     plt.imshow(cam_j_all, interpolation='none')
#     plt.colorbar()
#     plt.title(f"total events on {cam}")
#     plt.show()
# --------------------------------------------------------------------------------------------------

# SOMMA DEI FOTONI IN OGNI CAMERA PER UN DETERMINATO EVENTO
def SumPhotonsCam1event():
    all_cam_list = []#l'idea è fare un isto con tutte le camere e per ogni camera il numero di fotoni
    event_i = file[151][1]
    for cam in event_i:
        if np.any(event_i[cam] != 0.):
            #print(event_i_cam)
            sum_cam_all = sum(map(sum, event_i[cam]))
            all_cam_list.append(sum_cam_all)
    return all_cam_list

def HistoSumPhotonsCam1event():
    all_cam_list = SumPhotonsCam1event()
    plt.hist(all_cam_list, 100)
    plt.title(f"# photons of event {file[151][0]} in each camera")
    plt.show()

# HistoSumPhotonsCam1event()
# -------------------------------------------------------------------------------------------------------

# SOMMA DEI FOTONI IN OGNI CAMERA PER OGNI EVENTO. RITORNA UN ARRAY CHE CONTINE LA SOMMA DEI FOTONI PER OGNI CAMERA PER OGNI EVENTO (LISTA DI LISTE)
def SumPhotonsAllCams():
    all_cam_ev = []
    for i in range(len(file)):
        all_cam_list = []
        sum_cam_all = [0.]#definisco questa lista perchè mi serve dopo
        event_i = file[i][1]# così sto considerando file, nell'evento i esimo, la parte di hits_map (che  un dict)
        for cam in event_i:
            sum_cam_all = sum(map(sum, event_i[cam]))#nella camera x faccio la somma dei fotoni su ogni pixel
            all_cam_list.append(sum_cam_all)#ogni somma di fotoni relativa a una camera la aggiungo in una lista di tutte le camere in ogni evento
        all_cam_ev.append(all_cam_list)
    return all_cam_ev
        
        
def HistoSumPhotonsAllCams():
    all_cam_ev = SumPhotonsAllCams()
    for i in range(len(file)):
        if np.any(all_cam_ev[i]):
            plt.hist(all_cam_ev[i], 100)
            plt.title(f"# photons of event {file[i][0]} in each camera")
            plt.show()

#SumPhotonsAllCams()
# HistoSumPhotonsAllCams()
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

# SCATTER PLOT PER UN SINGOLO EVENTO -----------------------------------------------------------------------------
def CamList():
    cam_list = []
    event_i = file[151][1]
    for cam in event_i:
        if np.any(event_i[cam] != 0.):
            cam_list.append(cam)
    return cam_list

all_cam_list = SumPhotonsCam1event()
cam_list = CamList()

def PlotSumPhotons1Cam():
    plt.scatter(cam_list, all_cam_list)
    plt.title(f"plot - # photons of event {file[151][0]} for each camera")
    plt.xticks(rotation = 45)
    plt.xlim(10, 40)
    plt.show()

# PlotSumPhotons1Cam()
# ------------------------------------------------------------------------------------------------------------------

# SCATTER PLOT SU TUTTE GLI EVENTI
all_cam_ev = SumPhotonsAllCams()
cam_list = CamList()

def PlotSumPhotonsAllCams():
    for i in range(len(file)):
        if np.any(all_cam_ev[i]):
            plt.scatter(cam_list, all_cam_ev[i])
            plt.title(f"plot - # photons of event {file[i][0]} for each camera")
            plt.xticks(rotation = 45)
            #plt.xlim(0, 30)
            plt.show()

# PlotSumPhotonsAllCams()
# ------------------------------------------------------------------------------------------------------

from sklearn import preprocessing
sum_photons_all_cams_all_ev = SumPhotonsAllCams()
#print(sum_photons_all_cams_all_ev)

#normalized_data = preprocessing.RobustScaler(with_centering=False,quantile_range=(25.,75.)).fit_transform(sum_photons_all_cams_all_ev)
transformer = RobustScaler().fit(sum_photons_all_cams_all_ev)
normalized_data = transformer.transform(sum_photons_all_cams_all_ev)
#if np.any(normalized_data != 0.):
#print(list(normalized_data))

if np.all(sum_photons_all_cams_all_ev) == np.all(normalized_data): 
    print("true")
  