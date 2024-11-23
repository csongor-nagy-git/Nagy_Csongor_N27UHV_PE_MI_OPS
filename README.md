﻿# Nagy_Csongor_N27UHV_PE_MI_OPS

## Bevezetés

A Diabetikus Retinopátia (DR) egy súlyos szemészeti betegség, amely a cukorbetegség következményeként alakulhat ki, és amely a retina ereit érinti, végső soron vaksághoz vezethet. A DR korai felismerése és megfelelő kezelése kulcsfontosságú a betegség progressziójának megállításában, ezért az automatikus képelemzés és a mélytanulás módszerei egyre nagyobb szerepet kapnak a detektálásában.

A beadandó célja egy olyan demo létrehozása, amely lehetővé teszi, hogy a felhasználó egy UI-on keresztül szemfenékfotót töltsön fel. A feltöltött képet megfelelő méretűvé alakítva egy CNN modell becslést ad a diabetikus retinopátia súlyosságáról az adott szemfenékfotón.

A projektben használt CNN modell a Diabetikus Retinopátia képeken történő felismerésére szolgál, de a modell mérete miatt nem lehetett GitHub-ra feltölteni. Ezért egy dummy modellt alkalmaztam, amely ugyanolyan formában adja outputot, mint az eredeti, míg a teljes modell és a tanítási folyamata a "model_training" notebookban található.

## Működés

A projekt az órán tanult architektúrát alkmazza, ahol a kommunikációt a back-end és a front-end között FastAPI biztosítja és a predikció híváshoz RabbitMQ is felhasználásra került. 

### 1. Lépés: Instal requirements
```
pip install -r requirements.txt
```

### 2. Lépés: Csatlakozás az MLFlow szerverhez
```
mlflow server
```

### 3. Lépés: Back end elindítása
A file a src/api mappában található
```
python back_end.py
```
### 4. Lépés: Commands elindítása
A file a src/api mappában található
```
python commands.py
```
### 5. Lépés: Front end elindítása
A file a src/api mappában található
```
streamlit run front_end.py
```
### 6. Lépés: Kép feltöltése UI-on
Példa kép megtalálható a data mappában

## További fájlok 
Mivel a tényleges modell TPU-n fut GoogleColab-on ezért csatoltam referenciaként egy-két kapcsolodó Notebok-ot. Illetve TPU-n futtatva nincs lehetőség MLFlow szerverhez való csatlakozáshoz, ezért van egy külön model_uploader.py, ami a modell feltöltésben segített MLFlow-ra. Végül ez nem lett használva, mivel túl nagyok a tényleges modellhez tartozó fájlok GitHubra való feltöltésre.
