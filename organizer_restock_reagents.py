# Adjust to whether to not you want to remove reagents from your bag if you have more than the desired amount
removeReagentsIfOverRestockToAmount = True

houseReagentsChestSerial = 0x43923CEA

import Misc, Items, Player, Target
from Scripts.utilities.items import FindItem, MoveItem, FindNumberOfItems
from Scripts.glossary.items.reagents import reagents, reagentsNecro
from Scripts.glossary.colors import colors
from Scripts import config

# Usage example: RestockReagents(50, ['magery', 'necro'])
def RestockReagents(restockTo, type = ['magery']):
    global removeReagentsIfOverRestockToAmount

    Misc.SendMessage('Hello there!')

    reagentsBagSharedValue = 'reagentsBag'
    
    reagentsBag = Target.PromptTarget( 'Select bag to move the reagents into' )

    # if not Misc.CheckSharedValue( reagentsBagSharedValue ):
    #     reagentsBag = Target.PromptTarget( 'Select bag to move the reagents into' )
    #     Misc.SetSharedValue( reagentsBagSharedValue, reagentsBag )

    # reagentsBag = Misc.ReadSharedValue( reagentsBagSharedValue )
    if reagentsBag == None or Items.FindBySerial( reagentsBag ) == None:
        Player.HeadMessage( colors[ 'red' ], 'Can\'t find reagents bag! Clearing stored bag, please run again' )
        Misc.RemoveSharedValue( reagentsBagSharedValue )
        return

    reagentsBag = Items.FindBySerial( reagentsBag )

    reagentsSource = Target.PromptTarget( 'Select container to restock from' )
    reagentsSource = Items.FindBySerial( reagentsSource )
    if reagentsSource == None or not reagentsSource.IsContainer:
        Player.HeadMessage( colors[ 'red' ], 'Invalid source container' )

    Items.UseItem( reagentsSource )
    Misc.Pause( config.dragDelayMilliseconds )

    # Switch reagent type
    regs = dict()
    for regType in type:
        if regType == 'necro':
            regs.update(reagentsNecro)
        elif regType == 'magery':
            regs.update(reagents)
    
    reagentItemIDs = [ regs[ reagent ].itemID for reagent in regs ]
    reagentsInBag = FindNumberOfItems( reagentItemIDs, reagentsBag )
    
    for reagent in regs:
        Misc.Pause(1000)
        currentReagent = regs[ reagent ]
        if reagentsInBag[ currentReagent.itemID ] == restockTo:
            continue
        elif reagentsInBag[ currentReagent.itemID ] < restockTo:
            reagentStackFromReagentsBag = FindItem( currentReagent.itemID, reagentsBag )
            reagentStackFromSourceContainer = FindItem( currentReagent.itemID, reagentsSource )
            if reagentStackFromReagentsBag == None:
                MoveItem( Items, Misc, reagentStackFromSourceContainer, reagentsBag, restockTo )
            else:
                MoveItem( Items, Misc, reagentStackFromSourceContainer, reagentsBag, restockTo - reagentStackFromReagentsBag.Amount )
        elif removeReagentsIfOverRestockToAmount:
            reagentStackFromReagentsBag = FindItem( currentReagent.itemID, reagentsBag )
            Misc.SendMessage( 'Removing %i %s' % ( reagentStackFromReagentsBag.Amount - restockTo, currentReagent.name ) )
            MoveItem( Items, Misc, reagentStackFromReagentsBag, reagentsSource, reagentStackFromReagentsBag.Amount - restockTo )
            
    Misc.SendMessage('Done!')
