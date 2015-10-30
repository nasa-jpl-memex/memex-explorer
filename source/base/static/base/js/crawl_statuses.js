var statuses = statuses || {};

(function(){

  /**
  * Crawl Dashboard interactions
  */
  statuses.buttons = {
    play: "playButton",
    stop: "stopButton",
    restart: "restartButton",
    kill: "forceStopButton",
    images: "dumpImages",
    cca: "common-crawl-dump",
    rounds: "rounds",
    log: "getCrawlLog",
    seeds: "getInitialSeeds",
  }

  /**
  * This object contains information on which buttons should be enabled or
  * disabled based on the status of the crawl.
  */
  statuses.states = {
    "NOT STARTED": {
      "disabled": [
        "stop",
        "restart",
        "kill",
        "images",
        "cca",
        "log",
      ],
      "enabled": [
        "play",
        "rounds",
        "seeds",
      ],
    },
    "STARTING": {
      "disabled": [
        "stop",
        "restart",
        "kill",
        "images",
        "cca",
        "play",
        "rounds",
      ],
      "enabled": [
        "log",
        "seeds",
      ],
    },
    "STARTED": {
      "disabled": [
        "play",
        "restart",
        "images",
        "cca",
        "rounds",
      ],
      "enabled": [
        "stop",
        "kill",
        "log",
        "seeds",
      ],
    },
    "INJECT": {
      "disabled": [
        "play",
        "restart",
        "images",
        "cca",
        "rounds",
      ],
      "enabled": [
        "stop",
        "kill",
        "log",
        "seeds",
      ],
    },
    "GENERATE": {
      "disabled": [
        "play",
        "restart",
        "images",
        "cca",
        "rounds",
      ],
      "enabled": [
        "stop",
        "kill",
        "log",
        "seeds",
      ],
    },
    "FETCH": {
      "disabled": [
        "play",
        "restart",
        "images",
        "cca",
        "rounds",
      ],
      "enabled": [
        "stop",
        "kill",
        "log",
        "seeds",
      ],
    },
    "PARSE": {
      "disabled": [
        "play",
        "restart",
        "images",
        "cca",
        "rounds",
      ],
      "enabled": [
        "stop",
        "kill",
        "log",
        "seeds",
      ],
    },
    "UPDATEDB": {
      "disabled": [
        "play",
        "restart",
        "images",
        "cca",
        "rounds",
      ],
      "enabled": [
        "stop",
        "kill",
        "log",
        "seeds",
      ],
    },
    "RESTARTING": {
      "disabled": [
        "play",
        "restart",
        "images",
        "cca",
        "rounds",
        "stop",
        "kill",
        "log",
        "seeds",
      ],
      "enabled": [
      ],
    },
    "SUCCESS": {
      "disabled": [
        "play",
        "stop",
        "kill",
      ],
      "enabled": [
        "restart",
        "images",
        "cca",
        "rounds",
        "log",
        "seeds",
      ],
    },
    "FAILURE": {
      "disabled": [
        "stop",
        "restart",
        "kill",
        "images",
        "cca",
        "play",
        "rounds",
      ],
      "enabled": [
        "log",
        "seeds",
      ],
    },
    "STOPPING": {
      "disabled": [
        "stop",
        "restart",
        "kill",
        "images",
        "cca",
        "play",
        "rounds",
      ],
      "enabled": [
        "log",
        "seeds",
      ],
    },
    "STOPPED": {
      "disabled": [
        "stop",
        "kill",
        "images",
        "cca",
        "play",
        "rounds",
      ],
      "enabled": [
        "restart",
        "log",
        "seeds",
      ],
    },
    "FINISHING": {
      "disabled": [
        "stop",
        "restart",
        "images",
        "cca",
        "play",
        "rounds",
      ],
      "enabled": [
        "log",
        "seeds",
        "kill",
      ],
    },
    "FORCE STOPPED": {
      "disabled": [
        "stop",
        "restart",
        "kill",
        "images",
        "cca",
        "play",
        "rounds",
      ],
      "enabled": [
        "log",
        "seeds",
      ],
    },
    "REDIS ERROR": {
      "disabled": [
        "stop",
        "kill",
        "images",
        "cca",
        "play",
        "log",
        "seeds",
      ],
      "enabled": [
        "restart",
        "rounds",
      ],
    },
    "CELERY ERROR": {
      "disabled": [
        "stop",
        "kill",
        "images",
        "cca",
        "play",
        "log",
        "seeds",
      ],
      "enabled": [
        "restart",
        "rounds",
      ],
    },
  }
})();
