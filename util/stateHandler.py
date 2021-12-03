from typing import Any, List, Optional
import pandas as pd
from util.datahandler import DataHandler
from enum import Enum, auto
from dataclasses import dataclass, field

from util.utils import SearchOptions

# LATER: this could be divided with nested classes for more order


class Step:
    class Handrit_URL(Enum):
        Preprocessing = auto()
        Processing = auto()
        Postprocessing = auto()

    class MS_by_Pers(Enum):
        Search_person = 1
        Store_Results = 2


class SearchState:
    @dataclass
    class MS_by_Pers:
        mss: List[str]
        ppl: List[str]
        mode: SearchOptions


class StateHandler:
    def __init__(self) -> None:
        self.currentData = pd.DataFrame()
        self.resultMode = ''
        self.currentURLs_str: str = ''
        self.currentURL_list: List[str] = []
        self.currentSURL: str = ''
        self.currentBURL = ''  # TODO: check what's still used
        self.URLType = ''
        # self.multiSearch = 'False'
        self.multiBrowse = 'False'
        self.joinMode = 'All'
        self.didRun = 'dnr'
        self.CitaviSelect: Any = []
        self.handrit_step: Step.Handrit_URL = Step.Handrit_URL.Preprocessing
        self.ms_by_pers_step: Step.MS_by_Pers = Step.MS_by_Pers.Search_person
        self.postStep = ''
        self.currentCitaviData = pd.DataFrame()
        self.data_handler: DataHandler = None  # type: ignore
        self.search_ms_by_person_result_mss: List[str] = []
        self.search_ms_by_person_result_ppl: List[str] = []
        self.search_ms_by_person_result_mode: SearchOptions = SearchOptions.CONTAINS_ALL
