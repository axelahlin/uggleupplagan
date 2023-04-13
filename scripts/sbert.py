from sentence_transformers import SentenceTransformer, util
import wikipedia_fetcher as wf
model = SentenceTransformer('all-MiniLM-L6-v2')

# Two lists of sentences
sentences1 = ['Det är fint väder idag',
             'A man is playing guitar']#,
             #'The new movie is awesome', 'Lat. Aquisgranum, fr. Aix-la-Chapelle) Hufvudort i nyssnämnda område, vid den lilla ån Worm l. Wurm, nära gränsen till Holland och Belgien. 135,245 inv. (1900), däraf öfver 120,000 katoliker. A. är en af Tysklands äldsta historiska städer. Redan romarna kände dess hälsokällor, och ännu finnas där kvarlefvor af romerska bad. ',wf.get_text("Älmhult")[:100]]

sentences2 = ['Det är vackert väder idag',
              'A woman watches TV',
              'The new movie is so great'#,
              ]#' (Lat. Aquisgranum, fr. Aix-la-Chapelle) Hufvudort i nyssnämnda område, vid den lilla ån Worm l. Wurm, nära gränsen till Holland och Belgien. 135,245 inv. (1900), däraf öfver 120,000 katoliker. A. är en af Tysklands äldsta historiska städer. Redan romarna kände dess hälsokällor, och ännu finnas där kvarlefvor af romerska bad. Större betydelse fick A. genom Karl den store, som var född där och dog där samt där byggde ett palats och ett kapell (sedermera domkyrkan). Det var residensstaden i hans rike. I A. kröntes de tyske konungarna (från Ludvig den fromme 814 till Ferdinand I 1531). I A. slöts 1668 den fred, till hvilken Ludvig XIV tvungits genom trippelalliansen; 1748 slöts där en andra fred, somafslutade österrikiska successionskriget. A., som','köping i Kronobergs län, Allbo härad, vid Södra stambanan och ändpunkten för den 72 km. långa enskilda järnvägen Sölvesborg-Olofström-E. Genom k. br. 6 febr. 1885 blef E. municipalsamhälle, innefattande jämte E. järnvägsstation de egor af kronoskattehemmanet E., som begränsas i s. af hemmanet Froafälle, i v. af hemmanet Klöxhult, i n. af hemmanet Gemön och i ö. af en linje, dragen 297 m. ö. om den nuv. landsvägen, samt genom k. br. 28 sept. 1900 en fr. o. m. 1901 i kommunalt hänseende från Stenbrohult skild köping med omförmälda område samt öfriga delar af hemmanet E. 1,025 inv. (1905). Tax.-v. 733,700 (1905), däraf 113,100 kr. för jordbruksfastighet. Köpingen utgör äfven eget skoldistrikt och, enl. k. br. 8 dec. 1904, en särskild kapellförsamling med tillsvidare gemensam kyrka och kyrkobetjäning med Stenbrohults församling. Platsen har gästgifvargård, telefonstation, läkare, apotek, bankkontor, några mindre fabriker, ett 20-tal handlande och närmare ett 40-tal handtverkare.']

#Compute embedding for both lists
embeddings1 = model.encode(sentences1, convert_to_tensor=True)
embeddings2 = model.encode(sentences2, convert_to_tensor=True)

#Compute cosine-similarities
cosine_scores = util.cos_sim(embeddings1, embeddings2)

#Output the pairs with their score
for i in range(len(sentences1)):
    print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))