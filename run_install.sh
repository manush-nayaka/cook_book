if [ "$1" == "install" ]; then
    pip install -r requirement.txt
elif [ "$1" == "run" ]; then
    cd cook_book
    python help_me_cook.py
else
    echo "the argument can one of install/run"
fi
