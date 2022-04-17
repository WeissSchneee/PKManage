Operating environment
	Python version: 3.7
	Django version: 3.2.12
Compiler
	Pycharm version 2021.3.3 (Professional Edition )


Please edit some following file to confirm you can running the code successfully.

1. In ParkingManageSystem\settings.py:
	EMAIL_HOST_USER = ""
please enter your Email address.

2. In PKManage\views.py:
	in acess( ) function:
	host = ''
please get your own API access token in Baidu intelligent cloud.

3. In PKManage\views.py:
	in report( ) function:
	send_mail( )
please input your own email address in from_email and recipient_list parameters.


