# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/01

Description:
ItemDefinition is a class to process the raw ItemDefinition data 

Copyright (c) 2018, PH01L

###############################################################################
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

>>> CHANGELOG:
    0.1.0       Base functionality
"""

__version__ = "0.1.0"

import os
import sys
import json
import datetime
import collections
import logging

# Pip install required
import requests
import mwparserfromhell
import dateparser

sys.path.append(os.getcwd())
import WikiaExtractor
import ItemBonuses

###############################################################################
# Helper methods
def _strcast(val):
    """ Convert value to string. """
    if val is None:
        return None
    return str(val)

def _intcast(val):
    """ Convert input to integer. """
    if val is None:
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        if val == "":
            return (0)
        if val[0] == "-":
            if val[1:].isdigit():
                return int(val)
        else:
            if val.isdigit():
                return int(val)

def _floatcast(val):
    """ Convert input to float. """
    if val is None:
        return None
    if isinstance(val, float):
        return val
    if isinstance(val, str):
        if val == "":
            return float(0.0)
        else:
            return float(val)                
                
def _boolcast(val):
    """ Convert value to boolean object. """
    if val is None:
        return None
    elif val in ["True", "true", True, "Yes", "yes"]:
        return True
    elif val in ["False", "false", False, "No", "no"]:
        return False   

def _datecast(val):
    """ Check date by converting to datetime object, and convert back to str. """
    if val is None:
        return None
    elif val is "":
        return None
    elif isinstance(val, datetime.date):
        return val.strftime("%d %B %Y")
    try:
        date = datetime.datetime.strptime(val, "%d %B %Y")   
        return date.strftime("%d %B %Y")
    except:
        print("  > %s" % val)
        val = input("  > Enter a correct date: ")
        return _datecast(val)      

def _questcast(val):
    """ Convert quest entry to boolean. """
    if val is None:
        return None
    elif val:
        return _boolcast(True)
    else:
        return _boolcast(False)

###############################################################################
# ItemDefinition object
class ItemDefinition(object):
    def __init__(self, itemID, itemJSON, wikia_item_page_ids, wiki_buy_limits):
        # Input itemID number
        self.itemID = itemID
        # Input JSON file (from RuneLite ItemScraper)
        self.itemJSON = itemJSON

        # Bulk dict of all OSRS Wikia Item pages
        self.wikia_item_page_ids = wikia_item_page_ids
        # Bulk dict of all OSRS Wikia Item buy_limits
        self.wiki_buy_limits = wiki_buy_limits

        # TODO: Not sure what this is used for now
        self.object = None
        
        # Dict of all ItemDefinition properties
        self.properties = {
            "id" : None,
            "name" : None,
            "tradeable" : None,
            "stackable" : None,
            "noteable" : None,
            "equipable" : None,
            "members" : None,
            "weight" : None,
            "buy_limit" : None,
            "quest_item" : None,
            "release_date" : None,
            "cost" : None,
            "lowalch" : None,
            "highalch" : None,
            "examine" : None,
            "url" : None}

        # Item Bonuses (if equipable)   
        self.itemBonuses = ItemBonuses.ItemBonuses(self.itemID)

        # Setup logging
        logging.basicConfig(filename="ItemDefinition.log",
                                 filemode='a',
                                 level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = _intcast(value)

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = _strcast(value)

    @property
    def tradeable(self):
        return self._tradeable
    @tradeable.setter
    def tradeable(self, value):
        self._tradeable = _boolcast(value)                		

    @property
    def stackable(self):
        return self._stackable
    @stackable.setter
    def stackable(self, value):
        self._stackable = _boolcast(value)  

    @property
    def noteable(self):
        return self._noteable
    @noteable.setter
    def noteable(self, value):
        self._noteable = _boolcast(value)

    @property
    def equipable(self):
        return self._equipable
    @equipable.setter
    def equipable(self, value):
        self._equipable = _boolcast(value)

    @property
    def members(self):
        return self._members
    @members.setter
    def members(self, value):
        self._members = _boolcast(value)

    @property
    def weight(self):
        return self._weight
    @weight.setter
    def weight(self, value):
        self._weight = _floatcast(value)

    @property
    def weight_equipped(self):
        return self._weight_equipped
    @weight_equipped.setter
    def weight_equipped(self, value):
        self._weight_equipped = _floatcast(value)

    @property
    def buy_limit(self):
        return self._buy_limit
    @buy_limit.setter
    def buy_limit(self, value):
        self._buy_limit = _intcast(value)

    @property
    def quest_item(self):
        return self._quest_item
    @quest_item.setter
    def quest_item(self, value):
        self._quest_item = _questcast(value)

    @property
    def release_date(self):
        return self._release_date
    @release_date.setter
    def release_date(self, value):
        self._release_date = _datecast(value)	
		 
    @property
    def cost(self):
        return self._cost
    @cost.setter
    def cost(self, value):
        self._cost = _intcast(value)	

    @property
    def lowalch(self):
        return self._lowalch
    @lowalch.setter
    def lowalch(self, value):
        self._lowalch = _intcast(value)	          
        
    @property
    def highalch(self):
        return self._highalch
    @highalch.setter
    def highalch(self, value):
        self._highalch = _intcast(value)	        	

    @property
    def store_price(self):
        return self._store_price
    @store_price.setter
    def store_price(self, value):
        self._store_price = _intcast(value)

    @property
    def seller(self):
        return self._seller
    @seller.setter
    def seller(self, value):
        self._seller = _strcast(value)

    @property
    def examine(self):
        return self._examine
    @examine.setter
    def examine(self, value):
        self._examine = _strcast(value)
	           
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, value):
        self._url = _strcast(value)

    # def __getattr__(self, attr):
    #     return self[attr]

    def populate(self):
        # sys.stdout.write(">>> Processing: %s\r" % self.itemID)
        print(">>>>>>>>>>>> Processing: %s" % self.itemID)

        # Start section in logger
        self.logger.debug("============================================ START")
        self.logger.debug("ItemID: %s" % self.itemID)
        # self.logger.debug("ItemName: %s" % self.name)

        # Set all values from JSON input file into ItemDefinition object
        self.id = self.itemJSON["id"]
        self.name = self.itemJSON["name"]
        self.tradeable = self.itemJSON["tradeable"]
        self.stackable = self.itemJSON["stackable"]
        self.noteable = self.itemJSON["noteable"]
        self.equipable = self.itemJSON["equipable"]
        self.members = self.itemJSON["members"]
        self.weight = self.itemJSON["weight"]
        self.buy_limit = self.itemJSON["buy_limit"]
        self.quest_item = self.itemJSON["quest_item"]
        self.release_date = self.itemJSON["release_date"]
        self.cost = self.itemJSON["cost"]
        self.lowalch = self.itemJSON["lowalch"]
        self.highalch = self.itemJSON["highalch"]
        self.examine = self.itemJSON["examine"]
        self.url = self.itemJSON["url"]

        # Extras
        self.weight_equipped = 0.0
        self.store_price = 0
        self.seller = ""


        # Log the initial JSON input
        self.logger.debug("Dumping first input...")
        self.logger.debug("Starting: print_pretty_debug_json")
        self.print_pretty_debug_json()

        # Set all values from ItemDefinition object to properties dict
        for prop in self.properties:
            self.properties[prop] = getattr(self, prop)

        # All properties from ItemScraper RuneLite plugin are now loaded
        # Time to fetch other information of OSRS Wikia

        # Try to find a OSRS Wikia page for this item 
        self.logger.debug("Starting: determine_wiki_page")
        has_wikia_page = self.determine_wiki_page()
        
        # has_wikia_page indicates if OSRS Wikia page was found

        if has_wikia_page:
            # This item has an OSRS Wikia page
            # Try to extract the InfoboxItem template
            self.logger.debug("Starting: extract_InfoboxItem")
            has_infobox_item = self.extract_InfoboxItem()
            if has_infobox_item:
                self.logger.debug("Item InfoBox extracted successfully")
            else:
                self.logger.critical("Item InfoBox extraction error.")
                print(">>>>>>>>>>>> CRITICAL: Item InfoBox extraction error")
        else:
            self.logger.warning("Item has no OSRS Wikia page. Setting default values.")
            print(">>>>>>>>>>>> WARNING: No OSRS Wiki Page: %s" % self.name)
            # TODO: Need to do something with items that have no OSRS Wikia page
            # Might not need to implement, as defaults should already be set on JSON import

        # Continue processing... but only if equipable
        if self.equipable:
            self.logger.debug("Item is equipable... Trying to fetch bonuses...")
            if has_wikia_page:
                self.logger.debug("Starting: extract_InfoBoxBonuses")
                has_infobox_bonuses = self.extract_InfoBoxBonuses()
                if has_infobox_bonuses:
                    self.logger.debug("Item InfoBox Bonuses extracted successfully")
                else:
                    self.logger.critical("Item InfoBox Bonuses extraction error.")
                    print(">>>>>>>>>>>> CRITICAL: Item InfoBox Bonuses extraction error")
            else:
                self.logger.critical("Item is equipable, but has not OSRS Wikia page. Need to manually fix this item.")
                print(">>>>>>>>>>>> CRITICAL: Equipable item has no bonuses")


        # Log the second JSON input
        self.logger.debug("Dumping second input...")
        self.logger.debug("Starting: print_pretty_debug_json")
        self.print_pretty_debug_json()

        self.logger.debug("============================================ END")

        # Finished. Return the entire ItemDefinition object
        return self

    def determine_wiki_page(self):
        # Log
        self.logger.debug("Searching for item in OSRS Wikia by name...")
        
        # Check if the item name is in the Wikia API Dump
        # Return True if found by self.name
        # Return False if not found
        if self.name in self.wikia_item_page_ids:
            self.logger.debug(">>> ITEM FOUND:")
            self.logger.debug("  > name: %s" % self.name)
            self.logger.debug("  > id: %s" % self.id)
            self.logger.debug("  > wikia pageid: %s" % self.wikia_item_page_ids[self.name])
            return True
        else:
            self.logger.debug(">>> ITEM NOT FOUND: %s" % self.name)
            self.logger.debug(">>> ITEM NOT FOUND: %s" % self.id)
            return False

    def strip_infobox(self, input):
        # Clean an passed InfoBox string
        input = input.strip()
        input = input.replace("[", "")
        input = input.replace("]", "")

        return input        

    def extract_InfoboxItem(self):
        # Example: http://oldschoolrunescape.wikia.com/api.php?action=parse&prop=wikitext&format=json&page=3rd_age_pickaxe
        self.logger.debug("  > Extracting infobox for item...")
        url = "http://oldschoolrunescape.wikia.com/api.php?action=parse&prop=wikitext&format=json&page=" + self.name
        result = requests.get(url)
        # If the url was found, set to object
        if result:
            url_name = self.name.replace(" ", "_")
            self.url = "http://oldschoolrunescape.wikia.com/wiki/" + url_name
        # Force fetched page to JSON
        data = result.json()
        # Extract the actual content
        input = data["parse"]["wikitext"]["*"]
        # Parse actual content using mwparser
        wikicode = mwparserfromhell.parse(input)
        # Extract templates in the page
        templates = wikicode.filter_templates()
        self.logger.debug("Extracting Wikia InfoBox templates...")
        self.logger.debug(templates)
        for template in templates:
            # self.logger.debug(template)
            template_name = template.name.strip()
            template_name = template_name.lower()
            if "infobox item" in template_name:
                self.logger.debug("InfoBox Name: %s" % template_name)
                self.logger.debug("InfoBox FOUND... Continuing...")
                self.logger.debug("Starting: parse_InfoboxItem")
                # If the InfoboxItem template is found...
                # Parse it!
                self.parse_InfoboxItem(template)
                return True
            else:
                self.logger.debug("InfoBox Name: %s" % template_name)
                self.logger.debug("InfoBox NOT FOUND... Trying next entry...")
        return False                   

    def clean_weight(self, input):
        i_weight = None # Inventory weight
        e_weight = None # Equipped weight
        input = str(input)
        input = input.strip()
        # Fix for weight ending in kg, or space kg
        if input.endswith(" kg"):
            input = input.replace(" kg", "")
        if input.endswith("kg"):
            input = input.replace("kg", "")
        if "kg" in input:
            input = input.replace("kg", "")
        # Some items have Inventory/Equipped weights:
        # ValueError: could not convert string to float: "'''Inventory:''' 0.3{{kg}}<br> '''Equipped:''' -4.5"
        if "Inventory" in input:
            input = input.replace("'''", "")
            input = input.replace("{", "")
            input = input.replace("}", "")
            weight_list = input.split("<br>")
            i_weight = weight_list[0]
            i_weight = i_weight.replace("Inventory:", "")
            i_weight = i_weight.strip()
            e_weight = weight_list[1]
            e_weight = e_weight.replace("Equipped:", "")
            e_weight = e_weight.strip()
        else:
            i_weight = input
            e_weight = input

        return i_weight, e_weight

    def parse_InfoboxItem(self, template):
        self.logger.debug("Processing InfoBox template...")
        self.logger.debug(template)
        quest = self.strip_infobox(template.get("quest").value)
        self.quest_item = quest
        i_weight, e_weight = self.clean_weight(template.get("weight").value)
        self.weight = i_weight
        self.weight_equipped = e_weight
        release = self.strip_infobox(template.get("release").value)
        release = dateparser.parse(release)
        self.release_date = release
        examine = self.strip_infobox(template.get("examine").value)
        self.examine = examine
        if not self.tradeable:
            self.buy_limit = -1
        else:
            self.buy_limit = 0
        try:
            store_price = self.strip_infobox(template.get("store").value)
            self.store_price = store_price      
        except ValueError:
            self.store_price = -1
        try:
            seller = self.strip_infobox(template.get("seller").value)
            self.seller = seller   
        except ValueError:
            self.seller = ""

    def extract_InfoBoxBonuses(self):
        # Example: http://oldschoolrunescape.wikia.com/api.php?action=parse&prop=wikitext&format=json&page=3rd_age_pickaxe
        self.logger.debug("  > Extracting infobox for bonuses...")
        url = "http://oldschoolrunescape.wikia.com/api.php?action=parse&prop=wikitext&format=json&page=" + self.name
        result = requests.get(url)
        # Force fetched page to JSON
        data = result.json()
        # Extract the actual content
        input = data["parse"]["wikitext"]["*"]
        # Parse actual content using mwparser
        wikicode = mwparserfromhell.parse(input)
        # Extract templates in the page
        templates = wikicode.filter_templates()
        self.logger.debug("Extracting Wikia InfoBox BONUSES template...")
        self.logger.debug(templates)
        for template in templates:
            template_name = template.name.strip()
            template_name = template_name.lower()
            if "bonuses" in template_name:
                self.logger.debug("InfoBox Name: %s" % template_name)
                self.logger.debug("InfoBox FOUND... Continuing...")
                self.logger.debug("Starting: parse_InfoboxBonuses")
                # If the InfoboxItem template is found...
                # Parse it!
                self.parse_InfoboxBonuses(template)
                return True
            else:
                self.logger.debug("InfoBox Name: %s" % template_name)
                self.logger.debug("InfoBox NOT FOUND... Returning...")
        return False           
		
    def parse_InfoboxBonuses(self, template):
        self.logger.debug("Processing InfoBox template...")
        self.logger.debug(template)
        itemBonuses = ItemBonuses.ItemBonuses(self.itemID)
        itemBonuses.attack_stab = self.strip_infobox(template.get("astab").value)
        itemBonuses.attack_slash = self.strip_infobox(template.get("aslash").value)
        itemBonuses.attack_crush = self.strip_infobox(template.get("acrush").value)
        itemBonuses.attack_magic = self.strip_infobox(template.get("amagic").value)
        itemBonuses.attack_ranged = self.strip_infobox(template.get("arange").value)
        itemBonuses.defence_stab = self.strip_infobox(template.get("dstab").value)
        itemBonuses.defence_slash = self.strip_infobox(template.get("dslash").value)
        itemBonuses.defence_crush  = self.strip_infobox(template.get("dcrush").value)
        itemBonuses.defence_magic = self.strip_infobox(template.get("dmagic").value)
        itemBonuses.defence_ranged = self.strip_infobox(template.get("astab").value)
        itemBonuses.melee_strength = self.strip_infobox(template.get("drange").value)
        itemBonuses.ranged_strength = self.strip_infobox(template.get("rstr").value)
        itemBonuses.magic_damage = self.strip_infobox(template.get("mdmg").value)
        itemBonuses.prayer = self.strip_infobox(template.get("prayer").value)
        try:
            itemBonuses.attack_speed = self.strip_infobox(template.get("aspeed").value) 
        except ValueError:
            itemBonuses.attack_speed = -1       
        try:
            itemBonuses.slot  = self.strip_infobox(template.get("slot").value)
        except ValueError:
            itemBonuses.slot = ""
            self.logger.critical("Could not determine equipable item slot")        
        self.itemBonuses = itemBonuses
          
    ###########################################################################
    # Handle item to JSON
    def print_json(self):
        # Print JSON to console
        self.construct_json()
        json_obj = json.dumps(self.json_out)
        print(json_obj)

    def print_pretty_json(self):
        # Pretty print JSON to console
        self.construct_json()
        json_obj = json.dumps(self.json_out, indent=4)
        print(json_obj)

    def print_debug_json(self):
        # Print JSON to log file
        self.construct_json()
        json_obj = json.dumps(self.json_out)
        self.logger.debug(json_obj)

    def print_pretty_debug_json(self):
        # Pretty print JSON to log file
        self.construct_json()
        json_obj = json.dumps(self.json_out, indent=4)
        self.logger.debug(json_obj)
            
    def export_json(self):
        # Export JSON to individual file
        self.construct_json()
        out_fi = "item-json" + os.sep + str(self.id) + ".json"
        with open(out_fi, "w") as f:
            json.dump(self.json_out, f)

    def export_pretty_json(self):
        # Export pretty JSON to individual file
        self.construct_json()
        out_fi = "item-json" + os.sep + str(self.id) + ".json"
        with open(out_fi, "w") as f:
            json.dump(self.json_out, f, indent=4)

    def construct_json(self):
        self.json_out = collections.OrderedDict()
        self.json_out["id"] = self.id
        self.json_out["name"] = self.name
        self.json_out["tradeable"] = self.tradeable
        self.json_out["stackable"] = self.stackable
        self.json_out["noteable"] = self.noteable
        self.json_out["equipable"] = self.equipable
        self.json_out["members"] = self.members
        self.json_out["weight"] = self.weight
        self.json_out["buy_limit"] = self.buy_limit
        self.json_out["quest_item"] = self.quest_item
        self.json_out["release_date"] = self.release_date     
        self.json_out["cost"] = self.cost
        self.json_out["lowalch"] = self.lowalch
        self.json_out["highalch"] = self.highalch
        self.json_out["store_price"] = self.store_price
        self.json_out["seller"] = self.seller
        self.json_out["examine"] = self.examine
        self.json_out["url"] = self.url
        if self.equipable:
            self.json_out["weight_equipped"] = self.weight_equipped
            bonuses_in_json = self.itemBonuses.construct_json()
            self.json_out["bonuses"] = bonuses_in_json
            # Old code has item slot + weapon speed in main JSON body
            #self.json_out["item_slot"] = self.item_slot
            #if self.item_slot == "weapon" or self.item_slot == "two-handed":
            #    self.json_out["weapon_speed"] = self.weapon_speed
    
    def edit_json(self):
        """ Construct JSON, print JSON, manually check and edit the contents. """
        self.print_pretty_json()
        answer = input("Would you like to change a field? [y, N]: ")
        if answer.lower() == "y":
            field = input("Name of field to change: ")
            if field == "bonuses":
                subfield = input("Name of sub-field to change: ")
                subvalue = input("Enter new value for %s: " % subfield)
                self.bonuses[subfield] = subvalue
                self.check_json()
            else:
                value = input("Enter new value for %s: " % field)
                setattr(self, field, value)
            self.check_json()

    def check_json(self):
        """ Construct JSON, and auto check fields. """
        required_fields = ["id",
                           "name",
                           "tradeable",
                           "noteable",
                           "equipable",
                           "members",
                           "weight",
                           "buy_limit",
                           "quest_item",
                           "stackable",
                           "release_date", 
                           "cost",
                           "lowalch",
                           "highalch"]
                           # TODO: Update this list
        for field in required_fields:
            if not hasattr(self, field):
                print("ERROR: Missing object attribute for: %s" % field)
        # TODO: This code needs to be more thorough and in ItemBonuses class
        # if self.equipable:
        #     if not self.bonuses:
        #         print("ERROR: Equipable object has no item bonuses")
        #         quit()

################################################################################
if __name__=="__main__":
    # Run unit tests
    assert _intcast(-1) == -1
    assert _intcast("-1") == -1
  
    assert _boolcast("false") == False
    assert _boolcast("True")
    assert _boolcast("true")
    assert _boolcast(False) == False
    assert _boolcast(True)

    assert _strcast(1)
    assert _strcast("OSRS Rocks!")
    
    print("Module tests passed.")