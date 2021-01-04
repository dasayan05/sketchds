# GlyphAZZN Dataset

This is a large scale SVG-based font dataset released under [Google's Magenta project](https://magenta.tensorflow.org/), specifically in the paper titled [A Learned Representation for Scalable Vector Graphics](https://openaccess.thecvf.com/content_ICCV_2019/papers/Lopes_A_Learned_Representation_for_Scalable_Vector_Graphics_ICCV_2019_paper.pdf) accepted at ICCV 2019. The project/paper describes a generative model for learning representation of fonts and generate new fonts by sampling a latent vector. Although the code was released in Magenta's [repository](https://github.com/magenta/magenta/tree/master/magenta/models/svg_vae), the dataset was not published in its _original form_. Instead they published a [list of font files](https://storage.googleapis.com/magentadata/models/svg_vae/glyphazzn_urls.txt) to be added to a `parquetio` database and some pre-processing code to get `TFRecord` data structure out.

I wrote some utilities to download and preprocess the dataset into its intended original form (`SVG` format). This repository contains such tools and also few convenient utilities to visualize the fonts and use them in `PyTorch` under its `DataLoader` pipeline.

- [X] Downloading and preprocessing utility
- [ ] `PyTorch` data loader

## Downloading & Preprocessing

To download the font files used to build this dataset, run the following by pointing it to an empty directory `<empty-dir>`
```
python glyphazzn/download.py --outdir <empty-dir>
```

This will download all original font files (Of three different types: `ttf`, `otf` and `pfb`). Now you need to add them as your system font by doing

```
cp <EMPTYDIR>/ttf/* <EMPTYDIR>/otf/* <EMPTYDIR>/pfb/* ~/.fonts
fc-cache -fv
```

You need to place the fonts into a place where system can find them. I recommended putting them in `~/.fonts`. Now we can extract the individual glyphs (as `.svg`) of all fonts and their styles (`normal`, `bold`, `italic`, `bold-italic`) by doing

```
python glyphazzn/preprocessing.py --savedir <empty-dir>
```

Upon completion of the above command, the provided output directory will have the following folder structure

```
<directory>
|
|- <font1>
|    |- n  (a.svg, b.svg, .., A.svg, .. 1.svg)
|    |- b  (a.svg, b.svg, .., A.svg, .. 1.svg)
|    |- i  (a.svg, b.svg, .., A.svg, .. 1.svg)
|    |- ib (a.svg, b.svg, .., A.svg, .. 1.svg)
|- <font2>
|    |- n  (a.svg, b.svg, .., A.svg, .. 1.svg)
|   ...
|- <font3>
|   ...
```

Each folder named after an unique font will have 4 directories named `n`, `b`, `i` and `ib` for "normal", "bold", "italic" and "bold + italic" respectively which denotes 4 styling variations of the font. Each style folder will contain 26+26+10 glyphs for all alphanumeric characters (all in `.svg`). All SVG files will have just one [path element](https://www.w3schools.com/graphics/svg_path.asp) which can be parsed using Python's `svg.path` library.

The font glyphs look like this (some random glyphs are shown below):

| Fonts       | Glyphs                                                       |
| ----------- | ------------------------------------------------------------ |
| 4amdinner   | ![](./resources/4amdinner/0.svg)![](./resources/4amdinner/1.svg)![](./resources/4amdinner/A.svg)![](./resources/4amdinner/B.svg)![](./resources/4amdinner/a.svg)![](./resources/4amdinner/b.svg) |
| kabegnos    | ![](./resources/kabegnos/a.svg) ![](./resources/kabegnos/b.svg) ![](./resources/kabegnos/c.svg) ![](./resources/kabegnos/d.svg) ![](./resources/kabegnos/e.svg) ![](./resources/kabegnos/f.svg) |
| mobilesfont | ![](./resources/mobilesfont/0.svg) ![](./resources/mobilesfont/1.svg) ![](./resources/mobilesfont/a.svg) ![](./resources/mobilesfont/A.svg) ![](./resources/mobilesfont/b.svg) ![](./resources/mobilesfont/B.svg) |
| stargazer   | ![](./resources/stargazer/a.svg) ![](./resources/stargazer/b.svg) ![](./resources/stargazer/C.svg) ![](./resources/stargazer/D.svg) ![](./resources/stargazer/E.svg) ![](./resources/stargazer/f.svg) |
| whosfrank   | ![](./resources/whosfrank/A.svg) ![](./resources/whosfrank/b.svg) ![](./resources/whosfrank/C.svg) ![](./resources/whosfrank/d.svg) ![](./resources/whosfrank/K.svg) ![](./resources/whosfrank/W.svg) |