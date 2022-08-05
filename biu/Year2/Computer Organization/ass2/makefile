compile:
	gcc ex2.c -o a.out

testall: test1 test2 test3keep test3swap test1swap test2swap test3sk test3ss
	echo "done"

test1:	
	./a.out mac_input-utf-16.txt dst.txt
	cmp dst.txt mac_input-utf-16.txt
	./a.out unix_input-utf-16.txt dst.txt
	cmp dst.txt unix_input-utf-16.txt
	./a.out win_input-utf-16.txt dst.txt
	cmp dst.txt win_input-utf-16.txt

test2:
	./a.out mac_input-utf-16.txt dst.txt -mac -unix
	cmp dst.txt unix_input-utf-16.txt
	./a.out mac_input-utf-16.txt dst.txt -mac -win
	cmp dst.txt win_input-utf-16.txt
	./a.out mac_input-utf-16.txt dst.txt -mac -mac
	cmp dst.txt mac_input-utf-16.txt
	./a.out unix_input-utf-16.txt dst.txt -unix -mac
	cmp dst.txt mac_input-utf-16.txt
	./a.out unix_input-utf-16.txt dst.txt -unix -win
	cmp dst.txt win_input-utf-16.txt
	./a.out unix_input-utf-16.txt dst.txt -unix -unix
	cmp dst.txt unix_input-utf-16.txt
	./a.out win_input-utf-16.txt dst.txt -win -mac
	cmp dst.txt mac_input-utf-16.txt
	./a.out win_input-utf-16.txt dst.txt -win -unix
	cmp dst.txt unix_input-utf-16.txt
	./a.out win_input-utf-16.txt dst.txt -win -win
	cmp dst.txt win_input-utf-16.txt

test3keep:
	./a.out mac_input-utf-16.txt dst.txt -mac -unix -keep
	cmp dst.txt unix_input-utf-16_keep.txt
	./a.out mac_input-utf-16.txt dst.txt -mac -win -keep
	cmp dst.txt win_input-utf-16_keep.txt
	./a.out mac_input-utf-16.txt dst.txt -mac -mac -keep
	cmp dst.txt mac_input-utf-16_keep.txt
	./a.out unix_input-utf-16.txt dst.txt -unix -mac -keep
	cmp dst.txt mac_input-utf-16_keep.txt
	./a.out unix_input-utf-16.txt dst.txt -unix -win -keep
	cmp dst.txt win_input-utf-16_keep.txt
	./a.out unix_input-utf-16.txt dst.txt -unix -unix -keep
	cmp dst.txt unix_input-utf-16_keep.txt
	./a.out win_input-utf-16.txt dst.txt -win -mac -keep
	cmp dst.txt mac_input-utf-16_keep.txt
	./a.out win_input-utf-16.txt dst.txt -win -unix -keep
	cmp dst.txt unix_input-utf-16_keep.txt
	./a.out win_input-utf-16.txt dst.txt -win -win -keep
	cmp dst.txt win_input-utf-16_keep.txt

test3swap:
	./a.out mac_input-utf-16.txt dst.txt -mac -unix -swap
	cmp dst.txt unix_input-utf-16_swap.txt
	./a.out mac_input-utf-16.txt dst.txt -mac -win -swap
	cmp dst.txt win_input-utf-16_swap.txt
	./a.out mac_input-utf-16.txt dst.txt -mac -mac -swap
	cmp dst.txt mac_input-utf-16_swap.txt
	./a.out unix_input-utf-16.txt dst.txt -unix -mac -swap
	cmp dst.txt mac_input-utf-16_swap.txt
	./a.out unix_input-utf-16.txt dst.txt -unix -win -swap
	cmp dst.txt win_input-utf-16_swap.txt
	./a.out unix_input-utf-16.txt dst.txt -unix -unix -swap
	cmp dst.txt unix_input-utf-16_swap.txt
	./a.out win_input-utf-16.txt dst.txt -win -mac -swap
	cmp dst.txt mac_input-utf-16_swap.txt
	./a.out win_input-utf-16.txt dst.txt -win -unix -swap
	cmp dst.txt unix_input-utf-16_swap.txt
	./a.out win_input-utf-16.txt dst.txt -win -win -swap
	cmp dst.txt win_input-utf-16_swap.txt

test1swap:
	./a.out mac_input-utf-16_swap.txt dst.txt
	cmp dst.txt mac_input-utf-16_swap.txt
	./a.out unix_input-utf-16_swap.txt dst.txt
	cmp dst.txt unix_input-utf-16_swap.txt
	./a.out win_input-utf-16_swap.txt dst.txt
	cmp dst.txt win_input-utf-16_swap.txt

test2swap:
	./a.out mac_input-utf-16_swap.txt dst.txt -mac -unix
	cmp dst.txt unix_input-utf-16_swap.txt
	./a.out mac_input-utf-16_swap.txt dst.txt -mac -win
	cmp dst.txt win_input-utf-16_swap.txt
	./a.out mac_input-utf-16_swap.txt dst.txt -mac -mac
	cmp dst.txt mac_input-utf-16_swap.txt
	./a.out unix_input-utf-16_swap.txt dst.txt -unix -mac
	cmp dst.txt mac_input-utf-16_swap.txt
	./a.out unix_input-utf-16_swap.txt dst.txt -unix -win
	cmp dst.txt win_input-utf-16_swap.txt
	./a.out unix_input-utf-16_swap.txt dst.txt -unix -unix
	cmp dst.txt unix_input-utf-16_swap.txt
	./a.out win_input-utf-16_swap.txt dst.txt -win -mac
	cmp dst.txt mac_input-utf-16_swap.txt
	./a.out win_input-utf-16_swap.txt dst.txt -win -unix
	cmp dst.txt unix_input-utf-16_swap.txt
	./a.out win_input-utf-16_swap.txt dst.txt -win -win
	cmp dst.txt win_input-utf-16_swap.txt

test3sk:
	./a.out mac_input-utf-16_swap.txt dst.txt -mac -unix -keep
	cmp dst.txt unix_input-utf-16_swap.txt
	./a.out mac_input-utf-16_swap.txt dst.txt -mac -win -keep
	cmp dst.txt win_input-utf-16_swap.txt
	./a.out mac_input-utf-16_swap.txt dst.txt -mac -mac -keep
	cmp dst.txt mac_input-utf-16_swap.txt
	./a.out unix_input-utf-16_swap.txt dst.txt -unix -mac -keep
	cmp dst.txt mac_input-utf-16_swap.txt
	./a.out unix_input-utf-16_swap.txt dst.txt -unix -win -keep
	cmp dst.txt win_input-utf-16_swap.txt
	./a.out unix_input-utf-16_swap.txt dst.txt -unix -unix -keep
	cmp dst.txt unix_input-utf-16_swap.txt
	./a.out win_input-utf-16_swap.txt dst.txt -win -mac -keep
	cmp dst.txt mac_input-utf-16_swap.txt
	./a.out win_input-utf-16_swap.txt dst.txt -win -unix -keep
	cmp dst.txt unix_input-utf-16_swap.txt
	./a.out win_input-utf-16_swap.txt dst.txt -win -win -keep
	cmp dst.txt win_input-utf-16_swap.txt

test3ss:
	./a.out mac_input-utf-16_swap.txt dst.txt -mac -unix -swap
	cmp dst.txt unix_input-utf-16.txt
	./a.out mac_input-utf-16_swap.txt dst.txt -mac -win -swap
	cmp dst.txt win_input-utf-16.txt
	./a.out mac_input-utf-16_swap.txt dst.txt -mac -mac -swap
	cmp dst.txt mac_input-utf-16.txt
	./a.out unix_input-utf-16_swap.txt dst.txt -unix -mac -swap
	cmp dst.txt mac_input-utf-16.txt
	./a.out unix_input-utf-16_swap.txt dst.txt -unix -win -swap
	cmp dst.txt win_input-utf-16.txt
	./a.out unix_input-utf-16_swap.txt dst.txt -unix -unix -swap
	cmp dst.txt unix_input-utf-16.txt
	./a.out win_input-utf-16_swap.txt dst.txt -win -mac -swap
	cmp dst.txt mac_input-utf-16.txt
	./a.out win_input-utf-16_swap.txt dst.txt -win -unix -swap
	cmp dst.txt unix_input-utf-16.txt
	./a.out win_input-utf-16_swap.txt dst.txt -win -win -swap
	cmp dst.txt win_input-utf-16.txt

failtest:
	./a.out mac_input-utf-16.txt 
	./a.out mac_input-utf-16.txt dst.txt -unix
	./a.out mac_input-utf-16.txt -win -win -swap
	./a.out  mac_input-utf-16.txt -win
	./a.out mac_input-utf-16.txt dst.txt -win -swap
	./a.out mac_input-utf-16.txt dst.txt -swap
	./a.out aaaaaaaa.txt dst.txt -win -unix -keep