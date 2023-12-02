import re

# dump.py needs to exist, create with rq.py
from dump import *
# Alternatively create a fresh dump yourself:
# from rq import *

quests, items, npcs = {}, {}, {}

for message in messageDump:
    if 'Quest in dialog not present in QuestDB!' in message['content']:
        qid = int(re.search('Quest ID: (\d+)', message['content']).group(1))
        if qid == 0:
            continue
        if qid not in quests:
            quests[qid] = {'messages':[],'name':[],'text':[],'objectiveText':[],'rewardText':[],'xp':[],'questGiver':[],'coords':[]}
        quests[qid]['messages'].append(message)
        name = re.search('Quest Name: (.*?)\n', message['content']).group(1)
        if name != '' and name not in quests[qid]['name']:
            quests[qid]['name'].append(name)
        text = re.search('Quest Text: (.*?)\nObjective Text:', message['content'], re.DOTALL).group(1)
        if text != '' and text not in quests[qid]['text']:
            quests[qid]['text'].append(text)
        objectiveText = re.search('Objective Text: (.*?)\nReward Text:', message['content'], re.DOTALL).group(1)
        if objectiveText != '' and objectiveText not in quests[qid]['objectiveText']:
            quests[qid]['objectiveText'].append(objectiveText)
        rewardText = re.search('Reward Text: (.*?)\nReward XP:', message['content'], re.DOTALL).group(1)
        if rewardText != '' and rewardText not in quests[qid]['rewardText']:
            quests[qid]['rewardText'].append(rewardText)
        xp = int(re.search('Reward XP: (\d+)', message['content']).group(1))
        if xp != None and xp not in quests[qid]['xp']:
            quests[qid]['xp'].append(xp)
        questGiver = re.search('Questgiver: (.*?)\nPlayer Coords:', message['content'], re.DOTALL).group(1)
        if questGiver != '' and questGiver not in quests[qid]['questGiver']:
            quests[qid]['questGiver'].append(questGiver)
        coords = re.search('Player Coords:  (.*?)\nQuestLog:', message['content'], re.DOTALL).group(1)
        if coords != '' and coords not in quests[qid]['coords']:
            quests[qid]['coords'].append(coords)

    elif 'Targeted NPC not present in NPC DB!' in message['content']:
        nid = int(re.search('NPC ID: (\d+)', message['content']).group(1))
        if nid not in npcs:
            npcs[nid] = {'messages':[],'name':[]}
        npcs[nid]['messages'].append(message)
        name = re.search('NPC Name: (.*?)\n', message['content']).group(1)
        if name != '' and name not in npcs[nid]['name']:
            npcs[nid]['name'].append(name)

    elif 'Item not present in ItemDB!' in message['content']:
        iid = int(re.search('Item ID: (\d+)', message['content']).group(1))
        if iid not in items:
            items[iid] = {'messages':[],'name':[]}
        items[iid]['messages'].append(message)
        name = re.search('Item Name: \[(.*?)]\n', message['content']).group(1)
        if name != '' and name not in items[iid]['name']:
            items[iid]['name'].append(name)

questIDs = []
for k in quests:
    questIDs.append(k)
print(f'quests = {sorted(questIDs)}')

npcIDs = []
for k in npcs:
    npcIDs.append(k)
print(f'npcs = {sorted(npcIDs)}')

itemIDs = []
for k in items:
    itemIDs.append(k)
print(f'items = {sorted(itemIDs)}')

print(len(questIDs), len(npcIDs), len(itemIDs))


print('\n\nquestBlacklist = {')
for qid in sorted(quests):
    print(f'    {qid}, -- {quests[qid]["name"]}')

print('}\nnpcBlacklist = {')
for qid in sorted(npcs):
    print(f'    {qid}, -- {npcs[qid]["name"]}')

print('}\nitemBlacklist = {')
for qid in sorted(items):
    print(f'    {qid}, -- {items[qid]["name"]}')
print('}')
