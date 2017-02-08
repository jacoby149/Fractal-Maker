import pickle
import os

###saves data
def save(data):
    toSave = [data.fractalPoints,
    data.points,
    data.freeze,
    data.freezePoints,
    data.reticle,
    data.zoom,
    data.mode,
    data.sides
    ]
    with open('saves/'+data.selectedSave, 'wb') as fp:
        pickle.dump(toSave, fp)

###loads data
def load(data):
    with open ('saves/'+data.selectedSave, 'rb') as fp:
        load = pickle.load(fp)
    data.fractalPoints = load[0]
    data.points = load[1]
    data.freeze = load[2]
    data.freezePoints = load[3]
    data.reticle = load[4]
    data.zoom = load[5]
    data.mode = load[6]
    data.sides = load[7]

###deletes data
def delete(data):
    os.remove('saves/'+ data.selectedSave)

###gets save files as a list
def getAllSaves(data):
    allSaves = []
    for filename in os.listdir("saves"):
        allSaves.append(filename)
    return allSaves

###navigates up through list of saves
def upSelected(data):
    saves = getAllSaves(data)
    if data.selectedSave not in saves:
        index = 0
        data.selectedSave = saves[index] 
        return
    index = saves.index(data.selectedSave)
    index += 1
    if index < len(saves):
        data.selectedSave = saves[index] 

###navigates down through list of saves
def downSelected(data):
    saves = getAllSaves(data)    
    if data.selectedSave not in saves:
        index = 0
        data.selectedSave = saves[index] 
        return
    index = saves.index(data.selectedSave)
    index -= 1
    if index >= 0:
        data.selectedSave = saves[index] 

