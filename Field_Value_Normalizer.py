









import re;
from DB_Controller import DB_Controller;
import datetime;
import pandas;
from calendar import monthrange;

MONTH_MAP_DICT= {'January':"01", 'Jan':"01", 'February':"02", 'Feb':"02", 'March':"03", 'Mar':"03", 'April':"04", 'Apr':"04", 'May':"05", 'June':"06", 'Jun':"06", 'July':"07", 'Jul':"07", 'August':"08", 'Aug':"08",\
			 'September':"09", 'Sept':"09", 'October':"10", 'Oct':"10", 'November':"11", 'Nov':"11", 'December':"12", 'Dec':"12"};



def remove_characters(input_string, character_list):
	if input_string == None:
		return '';

	for item in character_list:
		input_string = re.sub(item,'',input_string);

	return input_string;

def remove_subregex(input_string, regex_string):
	input_string = re.sub(regex_string,'',input_string);
	return input_string;



def get_date_digits_for_gm(date_string):
	date_string = re.sub(r' +','',date_string);
	pattern_one = r'[A-Z]{1}[a-z]{2,}[ ,]{0,1}[0-9]{1,2}[ ,]{0,1}[0-9]{4}';
	if bool(re.search(pattern_one, date_string)):
		return date_string[re.search(pattern_one, date_string).start():re.search(pattern_one, date_string).end()];



def get_date_digits(date_string):
	date_string = date_string.strip();
	date_string = re.sub(",",'',date_string);
	date_string_word_list = re.split(r"[\s\,\.]",date_string);
	for word in date_string_word_list:
		# print word;
		for key in MONTH_MAP_DICT:
			if key == word:
				start_pos = re.search(key,date_string).start();
				date_string = re.sub(word,str(MONTH_MAP_DICT[key]),date_string[start_pos:]);
				date_string = re.sub('\s+',',',date_string);
				day_string = date_string.split(',')[1];
				if len(re.sub(' ','',day_string)) == 1:
					day_string = '0' + day_string;
				date_string = '-'.join([date_string.split(',')[2],date_string.split(',')[0],day_string]);
				date_string = remove_characters(date_string,['\.']);
				return date_string;
	
	for key in MONTH_MAP_DICT:
		if key in date_string:
			start_pos = re.search(key,date_string).start();
			end_pos = re.search(key,date_string).end();
			rest_date_string = date_string[end_pos:];
			month_string = MONTH_MAP_DICT[key];
			if len(rest_date_string) == 6:
				day_string = rest_date_string[:2];
				year_string = rest_date_string[-4:];
				return year_string + '-' + month_string + '-' + day_string;
			if len(rest_date_string) == 5:
				day_string = '0' + rest_date_string[:1];
				year_string = rest_date_string[-4:];
				return year_string + '-' + month_string + '-' + day_string; 

				
	return date_string;


def get_balance_digits(balance_string):
	balance_string = balance_string.strip();
	balance_string = re.sub(r"[\$\,]",'', balance_string);
	balance_string = re.sub(r"\(\d\)",'', balance_string);

	return balance_string;

descriptor_string_list = [];
def get_mapped_abbreviation_for_descriptor(descriptor_string):
	global descriptor_string_list;
	if len(descriptor_string_list) == 0:
		descriptor_string_list = DB_Controller.get_mapped_abbreviation_for_sponsor_from_db('Descriptors');

	for i in range(0, len(descriptor_string_list)):
		if descriptor_string_list.iloc[i]['Code'].strip() == descriptor_string:
			return descriptor_string_list.iloc[i]['Long_Nm'];
	return descriptor_string;


def get_normalized_descriptors(descriptor_string):
	# print descriptor_string;
	descriptor_string = re.sub(r"[\(\)\|\/]",' ',descriptor_string);
	descriptor_string = re.sub(r"FIX",'',descriptor_string);
	descriptor_string = re.sub(r" +",' ',descriptor_string);
	descriptor_string = re.sub(r"C II",'C',descriptor_string);
	descriptor_string = re.sub(r"C I",'C',descriptor_string);
	descriptor_string = re.sub(r"PACII",'PAC',descriptor_string);
	descriptor_string = re.sub(r"PACI",'PAC',descriptor_string);

	if descriptor_string.strip() == 'NPR NPR':
		descriptor_string = "R NPR";
	descriptor_string = descriptor_string.strip();
	# print descriptor_string;
	if ' ' not in descriptor_string:
		# print get_mapped_abbreviation_for_descriptor(descriptor_string);
		return get_mapped_abbreviation_for_descriptor(descriptor_string)

	return descriptor_string;


def get_sponsor_names(date_string):
	date_string = date_string.strip();
	date_string = re.sub(",",'',date_string);
	date_string_word_list = re.split(r"[\s\,\.]",date_string);
	for word in date_string_word_list:
		for key in MONTH_MAP_DICT:
			if key == word:
				start_pos = re.search(key,date_string).start();
				date_string = date_string[:start_pos];

	date_string = re.sub('\s+',' ',date_string);
	return date_string;

def get_day_count(day_count_string):
	day_count_string = day_count_string.strip();
	if '30' in day_count_string and '360' in day_count_string:
		day_count_string = '104';
	return day_count_string;

def get_deal_series(deal_string, prefix_str = ''):
	deal_string = deal_string.strip();
	if 'Series' in deal_string:
		deal_string = deal_string[re.search('Series',deal_string).end():];
		deal_string = re.sub(' ','',deal_string);
		deal_string = prefix_str + ' ' + deal_string;

	deal_string = re.sub(r'-0[1,]','-',deal_string);
	return deal_string;

def get_floater_index(pricing_formula):
	free_text = pricing_formula;
	free_text = free_text.upper();
	if 'LIBOR' in free_text:
		free_text = [item for item in free_text.split(' ') if 'LIBOR' in item][0];
		free_text = re.sub(r'[^A-Z0-9\-]','',free_text);
		if 'LIBOR' == free_text: return 'LIBOR01M'
		if 'YEAR' in free_text: return 'LIBOR12M'
		if 'MONTH' in free_text: return 'LIBOR01M'
		if '3' in free_text and 'ONE' not in free_text: return 'LIBOR03M'
		if 'THREE' in free_text: return 'LIBOR03M'
		if '6' in free_text: return 'LIBOR06M'
		if 'SEMI' in free_text: return 'LIBOR06M'
	else:
		return pricing_formula;

def get_floater_spread(pricing_formula):
	if bool(re.search(r"[0-9]{1,}.[0-9]{1,}", pricing_formula)):
		start_pos = re.search(r"[0-9]{1,}.[0-9]{1,}", pricing_formula).start();
		end_pos = re.search(r"[0-9]{1,}.[0-9]{1,}", pricing_formula).end();
		pricing_formula = pricing_formula[start_pos:end_pos+1];
		pricing_formula = re.sub('%','',pricing_formula);
		try:
			return str(float(pricing_formula) * 100);
		except:
			return pricing_formula;
	return pricing_formula;


def get_reset_frequency(original_str, floater_index_string):
	if '01M' in floater_index_string: return '12.0';
	if '03M' in floater_index_string: return '4.0';
	if '06M' in floater_index_string: return '2.0';
	if '12M' in floater_index_string: return '1.0';
	return original_str;


def get_pricing_speed(original_str):
	# print original_str;
	original_str = re.sub('%',' ',original_str);
	original_str = re.sub(r' +',' ',original_str);
	digits = original_str.strip().split(' ')[0];
	try:
		if len(digits) == 1:
			digits = digits + '.00';
			original_str = digits + ' ' + original_str.strip().split(' ')[1];
		if len(digits) == 2:
			digits = digits+'.0';
			original_str = digits + ' ' + original_str.strip().split(' ')[1];
		original_str = original_str.strip()
	except:
		print 'LOOOOOOOOOOOOK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',original_str;
	return original_str;


def get_structuring_ranges(original_str):
	if 'N/A' not in original_str:
		reged_result_list = re.findall(r'[0-9]{2,3}',original_str);
		original_str = ','.join(reged_result_list);
		if original_str is None or len(re.sub(' ','',original_str)) == 0:
			original_str = 'Please check the highlighted area for structuring range.';
		return original_str;
	else:
		original_str = 'Please check the highlighted area for structuring range.';
		return original_str;

all_names_list = [];
def get_mapped_abbreviation_for_sponsor(sponsor_string, field_type):
	abbreviation_list = [];
	original_str = sponsor_string;
	sponsor_string = re.sub(r'[^A-Za-z0-9]', '',sponsor_string).lower();
	global all_names_list;
	if len(all_names_list) == 0:
		if field_type == 1:
			all_names_list = DB_Controller.get_mapped_abbreviation_for_sponsor_from_db('Deal Manager');
		else:
			all_names_list = DB_Controller.get_mapped_abbreviation_for_sponsor_from_db('Trustee');
	else:
		pass;



	for i in range(0, len(all_names_list)):
		code = all_names_list.iloc[i]['Code'];
		long_nm = all_names_list.iloc[i]['Long_Nm'];
		long_nm = re.sub(r'[^A-Za-z0-9]', '',long_nm).lower();
		
		if long_nm in sponsor_string:
			print long_nm;
			start_pos = re.search(long_nm,sponsor_string).start();
			end_pos = re.search(long_nm,sponsor_string).end();
			# print '                    ',code, long_nm, start_pos, end_pos;
			covered_flag = 0;
			for temp_item in abbreviation_list:
				if start_pos >= temp_item[1] and end_pos <= temp_item[2] and not (start_pos == temp_item[1] and end_pos == temp_item[2]):
					covered_flag = 1;

			if covered_flag == 0:

				abbreviation_list.append([code, start_pos, end_pos]);
	
	if abbreviation_list == []:
		abbreviation_list.append([original_str,0,len(original_str)-1]);

	for item in abbreviation_list:
		print item;
	print sponsor_string;
	abbreviation_list = sorted(abbreviation_list, key=lambda x: (x[1]));
	return abbreviation_list;				
	# sys.exit();	

gm_managers_list = [];
def get_mapped_abbreviation_for_sponsor_gm(sponsor_string):

	original_str = sponsor_string;
	sponsor_string = re.sub(r'[^A-Za-z0-9]', '',sponsor_string).lower();
	sponsor_string = re.sub('incorporated','inc', sponsor_string);
	global gm_managers_list;
	if len(gm_managers_list) == 0:
		gm_managers_list = DB_Controller.get_mapped_abbreviation_for_sponsor_from_db('Deal Manager');
	else:
		pass;

	for i in range(0, len(gm_managers_list)):
		if sponsor_string == re.sub(r'[^A-Za-z0-9]', '',gm_managers_list.iloc[i]['Long_Nm']).lower():
			sponsor_string = gm_managers_list.iloc[i]['Code'].strip();
			return sponsor_string;

	return original_str;	



def get_mapped_abbreviation_for_sponsor_fm(sponsor_string):

	original_str = sponsor_string;

	original_str = original_str.strip();

	original_str_list = original_str.split('  ');

	# print original_str_list;

	try:
		sponsor_string = '';
		if 'The' in original_str_list[0]:
			sponsor_string = original_str_list[1];
		else:
			sponsor_string = original_str_list[0];

		first_sponsor_string = sponsor_string;	

		sponsor_string = re.sub(r'[^A-Za-z0-9]', '',sponsor_string).lower();
		sponsor_string = re.sub('incorporated','inc', sponsor_string);
		global gm_managers_list;
		if len(gm_managers_list) == 0:
			gm_managers_list = DB_Controller.get_mapped_abbreviation_for_sponsor_from_db('Deal Manager');
		else:
			pass;

		for i in range(0, len(gm_managers_list)):
			if sponsor_string == re.sub(r'[^A-Za-z0-9]', '',gm_managers_list.iloc[i]['Long_Nm']).lower():
				sponsor_string = gm_managers_list.iloc[i]['Code'].strip();
				print '          ---',sponsor_string;
				return sponsor_string;

		return first_sponsor_string;
	
	except:
		return original_str;	


def get_mapped_abbreviation_for_cosponsor_fm(sponsor_string):

	original_str = sponsor_string;

	original_str = original_str.strip();

	original_str_list = original_str.split('  ');

	# print original_str_list;

	if len(original_str_list) <= 2:
		return 'N/A, no co-sponsor found for this series. Please check the document';

	try:
		if 'The' in original_str_list[0]:
			return ' '.join(original_str_list[2:-1]);
		else:
			return ' '.join(original_str_list[1:-1]);
	
	except:
		return original_str;	


gm_trustees_list = [];
def get_mapped_abbreviation_for_trustee_gm(sponsor_string):

	original_str = sponsor_string;
	sponsor_string = re.sub(r'[^A-Za-z0-9]', '',sponsor_string).lower();
	global gm_trustees_list;
	if len(gm_trustees_list) == 0:
		gm_trustees_list = DB_Controller.get_mapped_abbreviation_for_sponsor_from_db('Trustee');
	else:
		pass;

	for i in range(0, len(gm_trustees_list)):
		if sponsor_string == re.sub(r'[^A-Za-z0-9]', '',gm_trustees_list.iloc[i]['Long_Nm']).lower():
			sponsor_string = gm_trustees_list.iloc[i]['Code'].strip();
			return sponsor_string;

	return original_str;	


def get_date_digits_without_day(date_string):
	date_string = date_string.strip();
	date_string = re.sub(",",'',date_string);

	month_string = '';


	for key in MONTH_MAP_DICT:
		if key in date_string:
			month_string = str(MONTH_MAP_DICT[key])
			
	year_string = date_string[re.search(r'[0-9]{4}',date_string).start():re.search(r'[0-9]{4}',date_string).end()];

	date_string = year_string + '-' + month_string;
	return date_string;

def get_last_business_day(flag_day = None):

  current_month = datetime.datetime.now().month;
  current_year = datetime.datetime.now().year;
  current_day = datetime.datetime.now().day;

  if flag_day is not None:
  	if current_day < flag_day:
  		current_month = current_month - 1;
  		if current_month == 0:
  			current_month = 12;
  			current_year = current_year - 1;

  start_month = '';
  end_month = '';

  if current_month != 12:
    start_month = str(current_month) + '/' + str(current_year);
    end_month = str(current_month+1) + '/' + str(current_year);
  else:
    start_month = str(current_month) + '/' + str(current_year);
    end_month = str(1) + '/' + str(current_year+1);

  r = pandas.date_range(start_month, end_month, period=12, freq='BM')[0].date()
  end_date = datetime.datetime.strptime(str(r),'%Y-%m-%d')

  return end_date.date()



def get_last_day_of_preceding_month(year, month):
	int_year = int(year);
	int_month = int(month);
	

	day = monthrange(int_year, int_month)[1];

	day = str(day);
	day = day if len(day) == 2 else '0'+day;



	return year + '-' + month + '-' + day;