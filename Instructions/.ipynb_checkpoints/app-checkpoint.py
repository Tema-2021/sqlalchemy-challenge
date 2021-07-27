{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 
   "metadata":{} null,
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "\n",
    "#Import Flask\n",
    "from flask import Flask, jsonify\n",
    "\n",
    "#################################################\n",
    "# Database Setup\n",
    "#################################################\n",
    "engine = create_engine(\"sqlite:///hawaii.sqlite\")\n",
    "\n",
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "# reflect the tables\n",
    "Base.prepare(engine, reflect=True)\n",
    "\n",
    "# Save reference to the table\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station\n",
    "\n",
    "#################################################\n",
    "# Flask Setup\n",
    "#################################################\n",
    "app = Flask(__name__)\n",
    "\n",
    "#################################################\n",
    "# Flask Routes\n",
    "#################################################\n",
    "\n",
    "@app.route(\"/\")\n",
    "def Homepage():\n",
    "    \"\"\"List all available api routes.\"\"\"\n",
    "    return (\n",
    "        f\"Available Routes:<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/<start><br/>\"\n",
    "        f\"/api/v1.0/<start>/<end>\"\n",
    "    )\n",
    "\n",
    "#################################################\n",
    "# Precipitation\n",
    "#################################################\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precipitation():\n",
    "    # Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "    \n",
    "\"\"\"Return a list of all precipitation measurement\"\"\"\n",
    "    # Query all precipitation measurement    \n",
    "    # Retrieve the data and precipitation scores\n",
    "results = session.query(Measurement.date, Measurement.prcp).\\\n",
    "        filter(Measurement.date >= last_year).\\\n",
    "        all()\n",
    "results\n",
    "\n",
    "session.close()\n",
    "# Convert list of tuples into normal list\n",
    "all_ppt = list(np.ravel(results))\n",
    "\n",
    "return jsonify(all_ppt)\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count":
   "metadata",
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
