import re

class messageDB():
    def __init__(self):
        self.db = {}
        self.objectDB = {'quests':{},'items':{},'npcs':{}}
        self.newestMessages = {}
        self.oldestMessages = {}

    def getOldestMessage(self, channel):
        if channel not in self.oldestMessages:
            return False
        return self.oldestMessages[channel]

    def getNewestMessage(self, channel):
        if channel not in self.newestMessages:
            return False
        return self.newestMessages[channel]

    def addDump(self, messageDump):
        """Add a list of Discord messages in JSON format to the Questie data"""
        added = 0
        skipped = 0
        for message in messageDump:
            if self.addMessage(message):
                added += 1
            else:
                skipped += 1
        print(f'Added {added} messages, skipped {skipped}.')

    def addMessage(self, message):
        """Adds Discord messages in JSON format to the Questie data"""
        # Update channel timestamps
        channel = message['channel_id']
        mid = message['id']
        timestamp = message['timestamp']
        if channel not in self.newestMessages:
            self.newestMessages[channel] = {'id':mid,'timestamp':timestamp}
        if timestamp > self.newestMessages[channel]['timestamp']:
            self.newestMessages[channel] = {'id': mid,'timestamp':timestamp}
        if channel not in self.oldestMessages:
            self.oldestMessages[channel] = {'id':mid,'timestamp':timestamp}
        if timestamp < self.oldestMessages[channel]['timestamp']:
            self.oldestMessages[channel] = {'id':mid,'timestamp':timestamp}
        # Create channel entry
        if channel  not in self.db:
            self.db[channel] = {}
        # Skip already known messages
        if mid in self.db[channel]:
            return False
        # Read relevant messages
        elif 'Targeted NPC not present in NPC DB!' in message['content']:
            self.db[channel][mid] = message
            return self.addNPC(message)
        elif 'Item not present in ItemDB!' in message['content']:
            self.db[channel][mid] = message
            return self.addItem(message)
        elif 'Quest in dialog not present in QuestDB!' in message['content'] or 'Quest in tracker not present in QuestDB!' in message['content']:
            self.db[channel][mid] = message
            return self.addQuest(message)
        # Skip all other messages
        else:
            return False
    
    def _searchValue(self, searchPattern, content, flags=0):
        """Finds a value in a Questie Debug dump and filters empty values"""
        value = re.search(searchPattern, content, flags)
        if value == None or value == '':
            return False
        else:
            return value.group(1)

    def _addValue(self, target, tid, key, value, locale=False):
        """Add a value to the internal DB and count it"""
        target = self.objectDB[target][tid][key]
        if value not in target:
            if locale:
                target[value] = {'locale':locale,'count':1}
            else:
                target[value] = 1
        else:
            if locale and target[value]['locale'] == 'unkn' and locale != 'unkn':
                target[value]['locale'] = locale
                target[value]['count'] += 1
            elif locale:
                target[value]['count'] += 1
            else:
                target[value] += 1

    def addNPC(self, message):
        npcs = self.objectDB['npcs']
        nid = re.search('NPC ID: (\d+)', message['content'])
        if nid == None:
            return False
        else:
            nid = int(nid.group(1))
        if nid not in npcs:
            npcs[nid] = {'messages':[],'name':{},'level':{},'health':{},'allegiance':{},'coords':{}}
        npcs[nid]['messages'].append((message['id'], message['channel_id']))
        locale = self._searchValue("Locale: (.*)\n?", message['content'])
        if not locale:
            locale = 'unkn'
        if name := self._searchValue('NPC Name: (.*?)\n', message['content']):
            self._addValue('npcs', nid, 'name', name, locale)
        if level := self._searchValue('NPC Level: (\d+)\n', message['content']):
            self._addValue('npcs', nid, 'level', level)
        if health := self._searchValue('NPC Health: (.*?)\n', message['content']):
            self._addValue('npcs', nid, 'health', int(health))
        if allegiance := self._searchValue('NPC Allegiance: (.*?)\nPlayer Coords', message['content']):
            self._addValue('npcs', nid, 'allegiance', allegiance)
        if coords := self._searchValue('Player Coords: (.*?)\n', message['content']):
            self._addValue('npcs', nid, 'level', level)
        return True

    def addItem(self, message):
        items = self.objectDB['items']
        iid = re.search('Item ID: (\d+)', message['content'])
        if iid == None or iid.group(1) == 0:
            return False
        else:
            iid = int(iid.group(1))
        if iid not in items:
            items[iid] = {'messages':[],'name':{},'questItem':{},'questStarter':{},'questID':{},'container':{},'coords':{}}
        items[iid]['messages'].append((message['id'], message['channel_id']))
        locale = self._searchValue("Locale: (.*)\n?", message['content'])
        if not locale:
            locale = 'unkn'
        if name := self._searchValue('Item Name: \[(.*?)]\n', message['content']):
            self._addValue('items', iid, 'name', name, locale)
        if questItem := self._searchValue('Quest Item: (.*?)\n', message['content']):
            self._addValue('items', iid, 'questItem', questItem)
        if questStarter := self._searchValue('Quest Starter: (.*?)\n', message['content']):
            self._addValue('items', iid, 'questStarter', questStarter)
        if questID := self._searchValue('Quest ID: (.*?)\n', message['content']):
            self._addValue('items', iid, 'questID', int(questID))
        if container := self._searchValue('Container: (.*?)\n', message['content']):
            self._addValue('items', iid, 'container', container)
        if coords := self._searchValue('Player Coords: (.*?)\n', message['content']):
            self._addValue('items', iid, 'coords', coords)
        return True

    def addQuest(self, message):
        quests = self.objectDB['quests']
        qid = re.search('Quest ID: (\d+)', message['content'])
        if qid == None or qid == 0:
            return False
        else:
            qid = int(qid.group(1))
        if qid not in quests:
            quests[qid] = {'messages':[],'name':{},'text':{},'objectiveText':{},'rewardText':{},'xp':{},'questGiver':{},'coords':{}}
        quests[qid]['messages'].append((message['id'], message['channel_id']))
        locale = self._searchValue("Locale: (.*)\n?", message['content'])
        if not locale:
            locale = 'unkn'
        if name := self._searchValue('Quest Name: (.*?)\n', message['content']):
            self._addValue('quests', qid, 'name', name, locale)
        if text := self._searchValue('Quest Text: (.*?)\nObjective Text:', message['content'], re.DOTALL):
            self._addValue('quests', qid, 'text', text, locale)
        if objectiveText := self._searchValue('Objective Text: (.*?)\nReward Text:', message['content'], re.DOTALL):
            self._addValue('quests', qid, 'objectiveText', objectiveText, locale)
        if rewardText := self._searchValue('Reward Text: (.*?)\nReward XP:', message['content'], re.DOTALL):
            self._addValue('quests', qid, 'rewardText', rewardText, locale)
        if xp := self._searchValue('Reward XP: (\d+)', message['content']):
            self._addValue('quests', qid, 'xp', int(xp))
        if questGiver := self._searchValue('Questgiver: (.*?)\n', message['content'], re.DOTALL):
            self._addValue('quests', qid, 'questGiver', questGiver)
        if coords := self._searchValue('Player Coords:  (.*?)\nQuestLog:', message['content'], re.DOTALL):
            self._addValue('quests', qid, 'coords', coords)
        return True
