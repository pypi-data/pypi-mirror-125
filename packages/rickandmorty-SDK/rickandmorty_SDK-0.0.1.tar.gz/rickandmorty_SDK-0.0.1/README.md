# rickandmorty_sdk


Acquisition of data from Rick and Morty characters through synchronous requests to the [Rick and Morty API](https://rickandmortyapi.com/)

Library with two options:
- List all characters: shows the names of all the characters and their identifier
- Show character info: by entering the identifier of a character, it shows the following information:
  - Name
  - Status
  - Species
  - Type
  - Gender
  - Origin
  - Location

Can be used as follows:

```py
import rickAndMortySDK as rams
```

Being able to access its functions in the following way:

```py
rams.listAllCharacters()
```

```py
rams.showCharacterInfo('id')
```