import sniff

sniff.db.create_all()
sniff.db.session.add(sniff.Person('Capitan Crunch'))
sniff.db.session.add(sniff.Person('Luke Skyworker'))
sniff.db.session.add(sniff.Person('Sir Lancelot'))
sniff.db.session.commit()