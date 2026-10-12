# Attribution: the population grid in this folder

`ghs_pop_e2030_0p25deg.npz` is a derivative of the Global Human Settlement Layer
(GHSL) population grid of the European Commission's Joint Research Centre (JRC).
It is shared under the Creative Commons Attribution 4.0 International licence
(CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), as its source is.

## Credit

The source data is GHS-POP R2023A, epoch 2030, European Commission, Joint
Research Centre. Cite both:

- the dataset: Schiavina, Freire, Carioli, MacManus (2023), GHS-POP R2023A,
  doi:10.2905/2FF68A52-5B5B-4A22-8F40-C41DA8332CFE;
- the reference paper for the release: Pesaresi et al. (2024), Advances on the
  Global Human Settlement Layer by joint assessment of Earth Observation and
  population survey data, International Journal of Digital Earth 17(1),
  doi:10.1080/17538947.2024.2390454.

The file's own `citation` string holds only the first.

The licence terms are the Commission's reuse policy (Decision 2011/833/EU):
reuse, redistribution and adaptation for any purpose, provided appropriate
credit is given, changes are indicated, and no endorsement is implied (GHSL,
"Use conditions and how to cite",
https://human-settlement.emergency.copernicus.eu/GHSLhowToCite.php, read
2026-09-28). Neither the European Commission nor the JRC endorses this
repository or its use of the data.

## The source file

`GHS_POP_E2030_GLOBE_R2023A_4326_30ss_V1_0.zip`, from the JRC open-data
server, 485,278,420 bytes, SHA-256
`f9ad1171aa71822a6a0c2e15179da34640fcd68e4c5f961b6603b22a7ec1f5d5`: residents
per 30 arc-second pixel, WGS84, for the 2030 epoch. The 2030 epoch is the JRC's
projection, not a census. The download is not in this repository.

## The change made

- **Summed from 30 arc-seconds to 0.25 degree.** Each 0.25 degree cell holds
  the total of the 30 arc-second pixels whose centres fall inside it. No value
  was modeled, smoothed or rescaled.
- **Two duplicate antimeridian columns dropped.** The source raster runs about
  two pixel columns past 360 degrees of longitude (its left edge sits at
  -180.008 degrees), so its two edge columns repeat the opposite side of the
  antimeridian. Only pixels whose centres fall in [-180, 180) degrees were
  kept, so no one is counted twice.

The result holds about 8.546 billion people.

## What the file holds

| Member | Content |
|---|---|
| `population` | people per 0.25 degree cell, float32, 720 rows by 1440 columns; rows run from 90N southward, columns from 180W eastward |
| `lat_top_deg` | 90.0, the grid's northern edge |
| `lon_left_deg` | -180.0, the grid's western edge |
| `cell_deg` | 0.25, the cell size in degrees |
| `source` | the source dataset and the change, as one string |
| `citation` | the dataset citation, as one string |

It loads with numpy's `allow_pickle=False`. The file is 705,701 bytes, SHA-256
`33a42880010757c1eb5c19ef6e092111753866b670d9bc38fa9e802aa8d12e25`. Why the
communications model ships it, and how it uses it, is
`docs/adr/009-demand-every-resident-on-a-shipped-grid.md`.
