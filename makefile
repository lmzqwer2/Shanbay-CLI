all:
	pyinstaller -F shanbay.py
install: all ~/.lshanbay cookie
	cp ./dist/shanbay ~/bin/shanbay
	cp cookie ~/.lshanbay/cookie
~/.lshanbay:
	mkdir ~/.lshanbay
cookie:
	touch cookie
uninstall:
	rm ~/bin/shanbay
	rm -r ~/.lshanbay
clean:
	rm -rf shanbay.spec dist/ build/
	rm cookie

.PHONY: all install uninstall clean
