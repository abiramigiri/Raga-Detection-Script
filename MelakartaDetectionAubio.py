def predictMelakarta(filename):
    import operator
    import sys
    from aubio import source, pitch
    import pandas as pd
    #Frequency ranges for each note from 1-13 were determined from a keyboard
    def note(pitch):
        if pitch < 58 or pitch > 74:
            return ""
        if 59.75 <= pitch <=60.25:
            return "1"
        if 60.75 <= pitch <=61.25:
            return "2"
        if 61.75 <= pitch <=62.25:
            return "3"
        if 62.75 <= pitch <=63.25:
            return "4"
        if 63.75 <= pitch <=64.25:
            return "5"
        if 64.75 <= pitch <=65.25:
            return "6"
        if 65.75 <= pitch <=66.25:
            return "7"
        if 66.75 <= pitch <=67.25:
            return "8"
        if 67.75 <= pitch <=68.25:
            return "9"
        if 68.75 <= pitch <=69.25:
            return "10"
        if 69.75 <= pitch <=70.25:
            return "11"
        if 70.75 <= pitch <=71.25:
            return "12"
        if 71.75 <= pitch <=72.25:
            return "13"
        return  ""

    notecount=dict({'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0,'13':0})

    downsample = 1
    samplerate = 44100 // downsample
    if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

    win_s = 2096 // downsample # fft size
    hop_s = 512  // downsample # hop size

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []

    # total number of frames read
    count=0
    notelist=['']
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        detected_note=note(pitch)
        if detected_note!='':
            if detected_note in notecount:
                notecount[detected_note]+=1
                if notelist[-1]!=detected_note:
                    notelist.append(detected_note)
            else:
                notecount[detected_note]=1
        pitches += [pitch]
        if read < hop_s: break

    notes=['1','8','13']
    sortednotes=[]
    for each in sorted(notecount.items(), key=lambda kv: kv[1]):
        sortednotes.append(each[0])

    swaracnt=2
    for each in sortednotes[::-1]:
        if each in ['2','3','4','5']:
            notes.append(each)
            swaracnt-=1
            if swaracnt==0:
                break

    swaracnt=2
    for each in sortednotes[::-1]:
        if each in ['9','10','11','12']:
            notes.append(each)
            swaracnt-=1
            if swaracnt==0:
                break

    if notecount['6']>notecount['7']:
        notes.append('6')
    else:
        notes.append('7')

    data=pd.read_csv("melakartas.csv")
    swaras=['1','2','3','4','5','6','7','8','9','10','11','12','13']
    for index in range(len(data)):
        yes=True
        for note in swaras:
            if (note in notes and data[note][index]==1) or (note not in notes and data[note][index]==0):
                pass
            else:
                yes=False
        if yes==True:
            converted_op=['0' for i in range(13)]
            for each in notes:
                converted_op[int(each)-1]='1'

            res=dict()
            res['detected']=' '.join(converted_op)
            converted_op=[]
            for i in range(13):
                converted_op.append(str(data[str(i+1)][index]))
            res['melakarta']=' '.join(converted_op)
            res['prediction']=data["Name"][index];
            print(res)
            return res
            break

#Call the function with the file you want to predict Raga for as argument
predictMelakarta("hari1.wav")
