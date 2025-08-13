# German4All
## Dataset and Models for German Paraphrasing into Different Complexity Levels

This repository contains the German4All dataset and code that was used to create it. The dataset and our fine-tuned model is uploaded to the HuggingFace hub for easier loading and usage. However, this link was removed for the blinded review.

## Dataset example
* Orig text: Die vier zum Teil beschädigten Nischenfiguren der Südfassade unterhalb des Giebels stellen Drama, Gesang, Musik und Tanz dar. Sie wurden von dem Stuttgarter Bildhauer Theodor Bausch geschaffen.
* Level 1: An einem großen Haus gibt es Figuren aus Stein. Sie sind ein bisschen kaputt. Die Figuren zeigen vier Dinge: ein Theaterstück, Singen, Musik und Tanzen. Ein Mann namens Theodor Bausch hat sie gemacht.  
-> LLM judge annotations: content_preservation = approximately, information_loss = often, information_addition = seldom,  complexity_level = a bit too complicated
* Level 2: An der Südseite eines Gebäudes gibt es vier beschädigte Statuen. Diese Statuen zeigen vier Künste: Schauspiel, Gesang, Musik und Tanz. Ein Künstler aus Stuttgart, Theodor Bausch, hat sie erschaffen.  
-> LLM judge annotations: content_preservation = approximately, information_loss = sometimes, information_addition = seldom,  complexity_level = a bit too easy
* Level 3: An der Südwand eines Gebäudes befinden sich vier teilweise beschädigte Statuen. Sie symbolisieren Dramatik, Gesang, Musik und Tanz. Diese Kunstwerke wurden vom Stuttgarter Bildhauer Theodor Bausch geschaffen.  
-> LLM judge annotations: content_preservation = correct, information_loss = seldom, information_addition = seldom,  complexity_level = appropriate
* Level 4:Die Südfassade des Gebäudes ziert eine Reihe von Nischenfiguren, die trotz teils sichtbarer Schäden die Künste des Dramas, Gesanges, der Musik und des Tanzes darstellen. Sie sind Werke des renommierten Stuttgarter Bildhauers Theodor Bausch.  
-> LLM judge annotations: content_preservation = correct, information_loss = never, information_addition = seldom,  complexity_level = appropriate
* Level 5: Die Südfassade des architektonischen Werkes weist vier beschädigte Nischenfiguren auf, welche die Disziplinen Drama, Gesang, Musik und Tanz repräsentieren. Diese künstlerischen Darstellungen wurden von Theodor Bausch, einem Bildhauer aus Stuttgart, gefertigt und reflektieren kulturelle Ausdrucksformen der bildenden Künste.  
-> LLM judge annotations: content_preservation = approximately, information_loss = sometimes, information_addition = often,  complexity_level = a bit too complicated

The samples are all of high quality. However, levels 3 and 4 achieve the best content preservation, while level 1 removes information ("Südfassade unterhalb des Giebels", "Stuttgarter") and level 5 adds information ("architektonischen Werkes", "reflektieren kulturelle Ausdrucksformen der bildenden Künste").
