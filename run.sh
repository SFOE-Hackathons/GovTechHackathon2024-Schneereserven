# script that downloads data for a given day, extracts
# the relevant regions, based on a polygon derived from geographical indicators
# and stores transformed data for the whole of Switzerland in a 
# file to run predictinons on 
#
# requires:
#   - the access keys to be exported in the shell
#   - the bucket name exported in the shell
#   - the starting date to be exported before running the script
#     (not really a pretty solution but it allows to parallelize the operation
#      we are in a hackathon after all right?)
#   - directories for storage to exists (mainly data/raw and data/prep)
#   - a dateranger pickle (that is, all dates that should be parsed)

# activate venv
source venv_snow_reserves/bin/activate

for i in {1..366}
do
    # use dataloader (makes it easier to manually parallelize)
    current_date=$(python src/main/dateranger.py)
    echo $current_date

    # load data
    python src/main/loader.py $current_date

    # transform data
    transform_file=(`ls data/raw/*.tif`)
    gdalwarp -t_srs EPSG:2056 $transform_file data/prep/transformed.tif

    # run extraction 
    python src/main/transformer.py $current_date

    # cleanup
    rm data/raw/*.tif
    rm data/prep/*.tif
done
