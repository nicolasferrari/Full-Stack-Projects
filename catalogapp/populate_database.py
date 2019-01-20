"""
Created on Mon Nov 26 14:47:36 2018

@author: Nicolas
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from project_database import Mineral, Base, Item, User

engine = create_engine('sqlite:///mineralsitemsusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Precious stones

user = User(name='nicolas', email='nferrari3444@gmail.com')
session.add(user)
session.commit()

mineral1 = Mineral(name='native elements', user_id=1)

session.add(mineral1)
session.commit()

item1 = Item(name='gold', origin='California, USA', colour='rich yellow',
             price='2.49', stones=mineral1, hardness='2.5-3',
             description='Gold'
             'is a chemical element with symbol Au (from Latin: aurum)'
             'and atomic number 79, making it one of the higher atomic'
             'number elements that occur naturally.'
             'In its purest form, it is a bright, slightly reddish'
             'yellow, dense, soft, malleable, and ductile'
             'metal. Chemically, gold is a transition metal'
             'and a group 11 element', user_id=1)

session.add(item1)
session.commit()

item2 = Item(name='silver', origin='worldwide', colour='grey',
             price='7.49', stones=mineral1, hardness='2.5-3',
             description='Silver is a chemical element with'
             'symbol Ag (from the Latin argentum, derived'
             'from the Proto-Indo-European  "shiny" or "white")'
             'and atomic number 47. A soft, white, lustrous'
             'transition metal, it exhibits the highest'
             'electrical conductivity, thermal conductivity',
             'and reflectivity of any metal', user_id=1)

session.add(item2)
session.commit()


item3 = Item(name='mercury', origin='Australia', colour='brown',
             price='5.5', stones=mineral1, hardness='3.3-5',
             description='Mercury is a chemical element with'
             'symbol Hg and atomic number 80. It is commonly'
             'known as quicksilver and was formerly named'
             'hydrargyrum . A heavy, silvery d-block element,'
             'mercury is the only metallic element that is'
             'liquid at standard conditions for temperature'
             'and pressure; the only other element that is'
             'liquid under these conditions is bromine,'
             'though metals such as caesium, gallium,'
             'and rubidium melt just above room temperature',
             user_id=1)

session.add(item3)
session.commit()


mineral2 = Mineral(name='oxides', user_id=1)

session.add(mineral2)
session.commit()

item1 = Item(name='sapphire', origin='India', colour='rich yellow',
             price='9.99', stones=mineral2, hardness='9',
             description='Sapphire is a precious gemstone,'
             'a variety of the mineral corundum, consisting'
             'of aluminium oxide with trace amounts of'
             'elements such as iron, titanium, chromium,'
             'copper, or magnesium. It is typically blue,'
             'but natural "fancy" sapphires also occur'
             'in yellow, purple, orange, and green colors;'
             '"parti sapphires" show two or more colors',
             user_id=1)

session.add(item1)
session.commit()

item2 = Item(name='hematite', origin='worldwide', colour='steel-grey',
             price='3.99', stones=mineral2, hardness='5-6',
             description='Hematite, also spelled as haematite,'
             'is the mineral form of iron(III) oxide , one of'
             'several iron oxides. It is the oldest known'
             'iron oxide mineral that has ever formed on'
             'earth, and is widespread in rocks and soils.'
             'Hematite crystallizes in the rhombohedral'
             'lattice system, and it has the same crystal'
             'structure as ilmenite and corundum',
             user_id=1)

session.add(item1)
session.commit()

item2 = Item(name='spinel', origin='worldwide',
             colour='black,blue,red,violet',
             price='3.99', stones=mineral2,
             hardness='7.5-8', description='Spinel'
             'is the magnesium aluminium member'
             'of the larger spinel group of minerals.'
             'It has the formula MgAl2O4 in the cubic'
             'crystal system.Spinel crystallizes in'
             'the isometric system; common crystal'
             'forms are octahedra, usually twinned.'
             'It has an imperfect octahedral cleavage'
             'and a conchoidal fracture. Its hardness'
             'is 8, its specific gravity is 3.5 4.1,'
             'and it is transparent to opaque with a'
             'vitreous to dull luster', user_id=1)

session.add(item2)
session.commit()

mineral3 = Mineral(name='Hidroxides', user_id=1)

session.add(mineral3)
session.commit()

item1 = Item(name='goethite', origin='Germany', colour='Yellowish',
             price='9.99', stones=mineral3, hardness='5-5.5',
             description='Goethite (FeO(OH) is an iron-bearing'
             'hydroxide mineral of the diaspore group. It is'
             'found in soil and other low-temperature environments.'
             'Goethite has been well known since ancient times'
             'for its use as a pigment (brown ochre). Evidence'
             'has been found of its use in paint pigment samples'
             'taken from the caves of Lascaux in France', user_id=1)

session.add(item1)
session.commit()

item2 = Item(name='brucite', origin='Inyo County, California USA',
             colour='white,greenish', price='2.99',
             stones=mineral3, hardness='2.5-3',
             description='Brucite is the mineral'
             'form of magnesium hydroxide, with'
             'the chemical formula Mg(OH)2. It'
             'is a common alteration product of'
             'periclase in marble; a low-temperature'
             'hydrothermal vein mineral in metamorphosed'
             'limestones and chlorite schists; and formed'
             'during serpentinization of dunites', user_id=1)

session.add(item2)
session.commit()

mineral4 = Mineral(name='Phosphates', user_id=1)

session.add(mineral4)
session.commit()

item1 = Item(name='apatite', origin='worldwide', colour='Various',
             price='2.99', stones=mineral4, hardness='5',
             description='Apatite is a group of phosphate'
             'minerals, usually referring to hydroxylapatite,'
             'fluorapatite and chlorapatite, with high'
             'concentrations of OH, F and Cl ions, respectively,'
             'in the crystal. The formula of the admixture of'
             'the three most common endmembers is written'
             'as Ca10(PO4)6(OH,F,Cl)2, and the crystal'
             'unit cell formulae of the individual'
             'minerals are written as Ca10(PO4)6(OH)2,'
             'Ca10(PO4)6F2 and Ca10(PO4)6Cl2', user_id=1)

session.add(item1)
session.commit()

item2 = Item(name='monazite', origin='Asia',
             colour='Yellowish to reddish brown,'
             'greenish', price='2.99', stones=mineral4,
             hardness='5-5.5', description='Monazite is'
             'a reddish-brown phosphate mineral containing'
             'rare-earth metals. It occurs usually in small'
             'isolated crystals. It has a hardness of 5.0 to'
             '5.5 on the Mohs scale of mineral hardness and'
             'is relatively dense, about 4.6 to 5.7 g/cm3.'
             'There are at least four different kinds of'
             'monazite, depending on relative elemental'
             'composition of the mineral', user_id=1)

session.add(item2)
session.commit()

mineral5 = Mineral(name='carbonates', user_id=1)

session.add(mineral5)
session.commit()

item1 = Item(name='calcite', origin='worldwide', colour='grey',
             price='0.75', stones=mineral5, hardness='3',
             description='Calcite is a carbonate mineral'
             'and the most stable polymorph of calcium'
             'carbonate (CaCO3). The Mohs scale of mineral'
             'hardness, based on scratch hardness comparison,'
             'defines value 3 as "calcite"', user_id=1)

session.add(item1)
session.commit()

item2 = Item(name='magnesite', origin='Brazil',
             colour='white, pale yellow, pale brown, faintly pink',
             price='7.49', stones=mineral5, hardness='4',
             description='Magnesite is a mineral with the'
             'chemical formula MgCO3 (magnesium carbonate).'
             'Iron, manganese, cobalt and nickel may occur'
             'as admixtures, but only in small amounts', user_id=1)

session.add(item2)
session.commit()

item3 = Item(name='dolomite', origin='France', colour='white,gray',
             price='5.5', stones=mineral1, hardness='3.5-4',
             description='Dolomite is an anhydrous carbonate'
             'mineral composed of calcium magnesium carbonate,'
             'ideally CaMg(CO3)2. The term is also used for a'
             'sedimentary carbonate rock composed mostly of'
             'the mineral dolomite. An alternative name sometimes'
             'used for the dolomitic rock type is dolostone', user_id=1)

session.add(item3)
session.commit()

mineral6 = Mineral(name='silicates', user_id=1)

session.add(mineral6)
session.commit()

item1 = Item(name='quartz', origin='worldwide, Brazil, China',
             colour='white', price='3.99', stones=mineral6,
             hardness='7', description='Quartz is a mineral'
             'composed of silicon and oxygen atoms in a'
             'continuous framework of SiO4 silicon oxygen'
             'tetrahedra, with each oxygen being shared'
             'between two tetrahedra, giving an overall'
             'chemical formula of SiO2. Quartz is the'
             'second most abundant mineral in Earths'
             'continental crust, behind feldspar', user_id=1)

session.add(item1)
session.commit()

item2 = Item(name='mica', origin='worlwide',
             colour='depend upon impurities',
             price='7.49', stones=mineral6,
             hardness='2.5-3.5', description='The mica'
             'group of sheet silicate (phyllosilicate)'
             'minerals includes several closely related'
             'materials having nearly perfect basal'
             'cleavage. All are monoclinic, with a'
             'tendency towards pseudohexagonal crystals,'
             'and are similar in chemical composition.'
             'The nearly perfect cleavage, which is the'
             'most prominent characteristic of mica, is'
             'explained by the hexagonal sheet-like'
             'arrangement of its atoms', user_id=1)

session.add(item2)
session.commit()

item3 = Item(name='epidote', origin='worlwide',
             colour='yellowish-green,black', price='3.99',
             stones=mineral6, hardness='6', description='Epidote'
             'is an abundant rock-forming mineral, but one of'
             'secondary origin. It occurs in marble and'
             'schistose rocks of metamorphic origin.'
             'It is also a product of hydrothermal'
             'alteration of various minerals (feldspars,'
             'micas, pyroxenes, amphiboles, garnets, and others)'
             'composing igneous rocks', user_id=1)

session.add(item3)
session.commit()

mineral7 = Mineral(name='Sulfates', user_id=1)

session.add(mineral7)
session.commit()

item1 = Item(name='baryte', origin='worldwide, Brazil, China',
             colour='white,grey', price='3.99', stones=mineral7,
             hardness='3-3.5', description='Baryte or barite is'
             'a mineral consisting of barium sulfate (BaSO4).'
             'Baryte is generally white or colorless, and is'
             'the main source of barium. The baryte group'
             'consists of baryte, celestine (strontium sulfate),'
             'anglesite (lead sulfate) and anhydrite (calcium sulfate).'
             'Baryte and celestine form a solid solution (Ba,Sr)SO4',
             user_id=1)

session.add(item1)
session.commit()

print("added minerals items!")