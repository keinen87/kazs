from django.db import models


class Organizations(models.Model):
    name = models.TextField()
    short_name = models.TextField()
    inn = models.TextField(blank=True, null=True)
    kpp = models.TextField(blank=True, null=True)
    contacts = models.TextField(blank=True, null=True)
    deleted = models.BigIntegerField()
    date_add = models.DateTimeField()
    date_delete = models.DateTimeField(blank=True, null=True)
    date_change_config = models.DateTimeField()
    acount_limit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    acount_state = models.TextField(blank=True, null=True)
    acount_state_date = models.DateTimeField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    show_on_map = models.IntegerField()
    extern_code = models.BigIntegerField()
    logo_file_path = models.TextField(blank=True, null=True)
    report_right_text = models.TextField(blank=True, null=True)
    report_bottom_text = models.TextField(blank=True, null=True)
    absolut_limit = models.BigIntegerField()
    balance_limit = models.DecimalField(max_digits=15, decimal_places=2)
    data_time_limit = models.DateTimeField()
    type_limit = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'organizations'


class GroupTanks(models.Model):
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'group_tanks'


class Tanks(models.Model):
    description = models.TextField(blank=True, null=True)
    section_count = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    id_organization = models.BigIntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    deleted = models.BigIntegerField()
    date_delete = models.DateTimeField(blank=True, null=True)
    id_group = models.ForeignKey(GroupTanks, models.DO_NOTHING, db_column='id_group', blank=True, null=True)
    extern_code = models.BigIntegerField()
    visible = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'tanks'


class FuelsType(models.Model):
    short_name = models.TextField()
    long_name = models.TextField()
    useinapp = models.BooleanField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    extern_code = models.BigIntegerField()
    measurement_units = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fuels_type'


class Cars(models.Model):
    number = models.TextField()
    model = models.TextField()
    type_auth = models.BigIntegerField()
    rfid_key_size = models.BigIntegerField()
    rfid_key = models.TextField()
    password = models.BigIntegerField()
    day_limit = models.BigIntegerField()
    month_limit = models.BigIntegerField()
    last_date = models.DateTimeField()
    deleted = models.BigIntegerField()
    date_add = models.DateTimeField()
    date_change_config = models.DateTimeField()
    date_delete = models.DateTimeField(blank=True, null=True)
    auth_user = models.BigIntegerField()
    id_org = models.ForeignKey(Organizations, models.DO_NOTHING, db_column='id_org', blank=True, null=True)
    contract = models.TextField(blank=True, null=True)
    extern_code = models.BigIntegerField()
    type_limit = models.IntegerField()
    absolut_limit = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cars'


class Users(models.Model):
    full_name = models.TextField()
    short_name = models.TextField()
    type_auth = models.BigIntegerField()
    rfid_key_size = models.BigIntegerField()
    rfid_key = models.TextField()
    type = models.BigIntegerField()
    admin_controller = models.BigIntegerField()
    day_limit = models.BigIntegerField()
    month_limit = models.BigIntegerField()
    last_date = models.DateTimeField()
    deleted = models.BigIntegerField()
    date_add = models.DateTimeField()
    date_change_config = models.DateTimeField()
    date_delete = models.DateTimeField(blank=True, null=True)
    auth_auto = models.BigIntegerField()
    id_org = models.ForeignKey(Organizations, models.DO_NOTHING, db_column='id_org', blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    contract = models.TextField(blank=True, null=True)
    input_odometr = models.IntegerField()
    adminfilltank = models.IntegerField()
    adminviewlevelmeters = models.IntegerField()
    adminoffsirena = models.IntegerField()
    extern_code = models.BigIntegerField()
    type_limit = models.IntegerField()
    absolut_limit = models.BigIntegerField()
    password_controller = models.BigIntegerField()
    password_soft = models.BigIntegerField()
    password_time_end = models.DateTimeField()
    password_change = models.DateTimeField()
    visible_all_controllers = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'users'


class Controllers(models.Model):
    address = models.BigIntegerField()
    date_change_config = models.DateTimeField()
    date_exchange = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    date_add = models.DateTimeField()
    scanning = models.BigIntegerField()
    deleted = models.BigIntegerField()
    date_delete = models.DateTimeField(blank=True, null=True)
    version_firmware = models.BigIntegerField()
    version_protocol = models.BigIntegerField()
    id_group = models.BigIntegerField()
    cpu_id1 = models.BigIntegerField()
    cpu_id2 = models.BigIntegerField()
    cpu_id3 = models.BigIntegerField()
    first_config_read = models.BigIntegerField()
    in_stop_mode = models.IntegerField()
    date_exchange_ok = models.DateTimeField()
    id_organization = models.BigIntegerField(blank=True, null=True)
    extern_code = models.BigIntegerField()
    serial_port_index = models.IntegerField()
    link_type_id = models.IntegerField()
    mode_intake = models.IntegerField()
    defaultsettings = models.IntegerField()
    levelup = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    levellow = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    leveluse = models.BooleanField(blank=True, null=True)
    temperaturaup = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    temperaturalow = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    temperaturause = models.BooleanField(blank=True, null=True)
    fillup = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    filllow = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    filluse = models.BooleanField(blank=True, null=True)
    allvolumeup = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    allvolumelow = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    allvolumeuse = models.BooleanField(blank=True, null=True)
    massup = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    masslow = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    massuse = models.BooleanField(blank=True, null=True)
    densityup = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    densitylow = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    densityuse = models.BooleanField(blank=True, null=True)
    fuelvolumeup = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fuelvolumelow = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fuelvolumeuse = models.BooleanField(blank=True, null=True)
    levelwaterup = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    levelwaterlow = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    levelwateruse = models.BooleanField(blank=True, null=True)
    control_level = models.IntegerField()
    video_server = models.TextField(blank=True, null=True)
    video_server_id_camera = models.IntegerField(blank=True, null=True)
    video_user = models.TextField(blank=True, null=True)
    video_pass = models.TextField(blank=True, null=True)
    status_connect = models.IntegerField()
    login_controller = models.TextField(blank=True, null=True)
    password_controller = models.TextField(blank=True, null=True)
    hash_v2 = models.BigIntegerField()
    countchangepassword_v2 = models.BigIntegerField()
    countresetpassword_v2 = models.BigIntegerField()
    typelevelmeters = models.BigIntegerField()
    levelmeter_veeder_root = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'controllers'


class GroupControllers(models.Model):
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'group_controllers'


class LevelMeters(models.Model):
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    number_on_controller = models.BigIntegerField()
    deleted = models.BigIntegerField()
    date_delete = models.DateTimeField(blank=True, null=True)
    type = models.BigIntegerField()
    address = models.BigIntegerField()
    polling_period = models.BigIntegerField()
    chart_point_max_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'level_meters'


class Sections(models.Model):
    id_tank = models.ForeignKey(Tanks, models.DO_NOTHING, db_column='id_tank')
    id_fuels_type = models.ForeignKey(FuelsType, models.DO_NOTHING, db_column='id_fuels_type')
    id_level_meter = models.BigIntegerField(blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    level_height_low = models.DecimalField(max_digits=10, decimal_places=2)
    level_height_up = models.DecimalField(max_digits=10, decimal_places=2)
    volume_low = models.DecimalField(max_digits=15, decimal_places=2)
    volume_up = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.DecimalField(max_digits=15, decimal_places=2)
    id_calibration = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    level_up = models.DecimalField(max_digits=10, decimal_places=2)
    level_low = models.DecimalField(max_digits=10, decimal_places=2)
    level_use = models.BooleanField()
    temperature_up = models.DecimalField(max_digits=10, decimal_places=2)
    temperature_low = models.DecimalField(max_digits=10, decimal_places=2)
    temperature_use = models.BooleanField()
    fill_up = models.DecimalField(max_digits=10, decimal_places=2)
    fill_low = models.DecimalField(max_digits=10, decimal_places=2)
    fill_use = models.BooleanField()
    all_volume_up = models.DecimalField(max_digits=15, decimal_places=2)
    all_volume_low = models.DecimalField(max_digits=15, decimal_places=2)
    all_volume_use = models.BooleanField()
    mass_up = models.DecimalField(max_digits=15, decimal_places=2)
    mass_low = models.DecimalField(max_digits=15, decimal_places=2)
    mass_use = models.BooleanField()
    density_low = models.DecimalField(max_digits=10, decimal_places=3)
    density_up = models.DecimalField(max_digits=10, decimal_places=3)
    density_use = models.BooleanField()
    fuel_volume_low = models.DecimalField(max_digits=15, decimal_places=2)
    fuel_volume_up = models.DecimalField(max_digits=15, decimal_places=2)
    fuel_volume_use = models.BooleanField()
    level_water_low = models.DecimalField(max_digits=10, decimal_places=2)
    level_water_up = models.DecimalField(max_digits=10, decimal_places=2)
    level_water_use = models.BooleanField()
    control_level = models.BigIntegerField()
    deleted = models.BigIntegerField()
    date_delete = models.DateTimeField(blank=True, null=True)
    peak_volume = models.DecimalField(max_digits=15, decimal_places=2)
    fuel_balance = models.DecimalField(max_digits=15, decimal_places=2)
    fuel_balance_controller = models.DecimalField(max_digits=15, decimal_places=2)
    date_read_controller = models.DateTimeField()
    volume_low_invoice = models.BigIntegerField()
    volume_delta = models.IntegerField()
    number_section = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'sections'


class Fillings(models.Model):
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    id_user = models.ForeignKey(Users, models.DO_NOTHING, db_column='id_user')
    id_car = models.ForeignKey(Cars, models.DO_NOTHING, db_column='id_car', blank=True, null=True)
    id_fuel = models.ForeignKey(FuelsType, models.DO_NOTHING, db_column='id_fuel')
    date_time = models.BigIntegerField()
    litre = models.DecimalField(max_digits=15, decimal_places=3)
    impulse = models.BigIntegerField()
    impulse_count = models.BigIntegerField()
    adjusting_factor = models.BigIntegerField()
    fill_dosimeter = models.BigIntegerField()
    power_off = models.BigIntegerField()
    id_tank = models.BigIntegerField()
    count_error_link = models.IntegerField()
    state_end = models.IntegerField()
    trk_error = models.IntegerField()
    level_data_start = models.IntegerField()
    level_data_end = models.IntegerField()
    sleeve = models.IntegerField()
    is_check_video = models.IntegerField(blank=True, null=True)
    id_video = models.BigIntegerField(blank=True, null=True)
    index_dispenser = models.BigIntegerField()
    side = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'fillings'


class CarsLimit(models.Model):
    id_car = models.ForeignKey(Cars, models.DO_NOTHING, db_column='id_car')
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    limit_month = models.DecimalField(max_digits=15, decimal_places=3)
    limit_day = models.DecimalField(max_digits=15, decimal_places=3)
    date_last_filling = models.DateTimeField()
    date_read = models.DateTimeField()
    type_limit = models.IntegerField()
    absolut_limit = models.DecimalField(max_digits=15, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'cars_limit'


class CarsLimit2(models.Model):
    id_car = models.ForeignKey(Cars, models.DO_NOTHING, db_column='id_car')
    limit_month = models.DecimalField(max_digits=15, decimal_places=3)
    limit_day = models.DecimalField(max_digits=15, decimal_places=3)
    date_last_filling = models.DateTimeField()
    date_read = models.DateTimeField()
    limit_changed = models.IntegerField()
    type_limit = models.IntegerField()
    absolut_limit = models.DecimalField(max_digits=15, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'cars_limit2'


class UsersLimit(models.Model):
    id_user = models.ForeignKey(Users, models.DO_NOTHING, db_column='id_user')
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    limit_month = models.DecimalField(max_digits=15, decimal_places=3)
    limit_day = models.DecimalField(max_digits=15, decimal_places=3)
    date_last_filling = models.DateTimeField()
    date_read = models.DateTimeField()
    type_limit = models.IntegerField()
    absolut_limit = models.DecimalField(max_digits=15, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'users_limit'


class UsersLimit2(models.Model):
    id_user = models.ForeignKey(Users, models.DO_NOTHING, db_column='id_user')
    limit_month = models.DecimalField(max_digits=15, decimal_places=3)
    limit_day = models.DecimalField(max_digits=15, decimal_places=3)
    date_last_filling = models.DateTimeField()
    date_read = models.DateTimeField()
    limit_changed = models.IntegerField()
    type_limit = models.IntegerField()
    absolut_limit = models.DecimalField(max_digits=15, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'users_limit2'


class Accounttransactions(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_org = models.BigIntegerField()
    comment = models.TextField(blank=True, null=True)
    sum = models.DecimalField(max_digits=15, decimal_places=2)
    deleted = models.BigIntegerField()
    date_add = models.DateTimeField()
    date_delete = models.DateTimeField(blank=True, null=True)
    date_change_config = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'accounttransactions'


class AutoReportConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    report_type_config = models.BigIntegerField()
    report_name_config = models.TextField()
    id_controllers = models.TextField(blank=True, null=True)
    id_users = models.TextField(blank=True, null=True)
    id_cars = models.TextField(blank=True, null=True)
    id_orgs = models.TextField(blank=True, null=True)
    id_org_sum = models.TextField(blank=True, null=True)
    id_org_transaction = models.TextField(blank=True, null=True)
    name_filter_org = models.TextField(blank=True, null=True)
    name_filter_group = models.TextField(blank=True, null=True)
    id_filter_sum = models.BigIntegerField(blank=True, null=True)
    id_org_config = models.BigIntegerField(blank=True, null=True)
    is_all = models.BigIntegerField()
    id_tanks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auto_report_config'


class ChangeParamTrkWork(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    id_user = models.ForeignKey(Users, models.DO_NOTHING, db_column='id_user')
    date_change = models.DateTimeField()
    type_change = models.IntegerField()
    param1 = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'change_param_trk_work'


class Changes(models.Model):
    # Удалена строка: id = models.BigAutoField()
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    date_time = models.DateTimeField()
    changes_type = models.IntegerField()
    applied = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'changes'


class Communication(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    id_tank = models.ForeignKey(Tanks, models.DO_NOTHING, db_column='id_tank')
    section1_sleeve = models.BigIntegerField()
    section2_sleeve = models.BigIntegerField()
    section3_sleeve = models.BigIntegerField()
    section4_sleeve = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'communication'


class ControllerCardReader(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    api_key = models.TextField(blank=True, null=True)
    term_info = models.TextField()

    class Meta:
        managed = False
        db_table = 'controller_card_reader'


class ControllerCars(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    id_car = models.ForeignKey(Cars, models.DO_NOTHING, db_column='id_car')
    needwrite = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'controller_cars'


class ControllerDates(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    date_exchange = models.DateTimeField()
    date_exchange_ok = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'controller_dates'


class ControllerEthernet(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    dhcp = models.BigIntegerField()
    lamac = models.BigIntegerField()
    ipaddresscontroller = models.TextField()
    masksubnetwork = models.TextField()
    gateway = models.TextField()
    dnsserver = models.TextField()
    physicaddressmac = models.TextField()
    lm_mode = models.BigIntegerField()
    lm_ipaddress = models.TextField()
    lm_port = models.BigIntegerField()
    lm_levelmeter = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'controller_ethernet'


class ControllerEthexternaldeviceio(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    index = models.BigIntegerField()
    ipaddressblock = models.TextField()
    countsensorspositioncrane = models.BigIntegerField()
    typebindingsensorpositioncraneofcontroller = models.BigIntegerField()
    fin1 = models.BigIntegerField()
    fin2 = models.BigIntegerField()
    fin3 = models.BigIntegerField()
    fin4 = models.BigIntegerField()
    fin5 = models.BigIntegerField()
    fin6 = models.BigIntegerField()
    fin7 = models.BigIntegerField()
    fin8 = models.BigIntegerField()
    fin9 = models.BigIntegerField()
    fin10 = models.BigIntegerField()
    bindingfuninput = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'controller_ethexternaldeviceio'


class ControllerInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    major_version = models.BigIntegerField()
    minor_version = models.BigIntegerField()
    hardware_revision_major = models.BigIntegerField()
    hardware_revision_minor = models.BigIntegerField()
    type = models.BigIntegerField()
    has_modem = models.BigIntegerField()
    flash_type = models.TextField()
    flash_size = models.BigIntegerField()
    fram_type = models.TextField()
    fram_size = models.BigIntegerField()
    max_users = models.BigIntegerField()
    date_manufacture = models.DateTimeField()
    serial = models.TextField(blank=True, null=True)
    max_orgs = models.BigIntegerField()
    gsm_type = models.TextField()
    gsm_version = models.TextField()
    version_struct_configuration = models.BigIntegerField()
    version_interface_firmware = models.BigIntegerField()
    version_interface_hardware = models.BigIntegerField()
    volt = models.BigIntegerField()
    version_loader = models.BigIntegerField()
    isinterfacepanel = models.BigIntegerField()
    isindicator = models.BigIntegerField()
    iskeyboard = models.BigIntegerField()
    isflowsensor = models.BigIntegerField()
    indicator_firmware = models.BigIntegerField()
    indicator_hardware = models.BigIntegerField()
    keyboard_firmware = models.BigIntegerField()
    keyboard_hardware = models.BigIntegerField()
    flowsensor_firmware = models.BigIntegerField()
    flowsensor_hardware = models.BigIntegerField()
    keyboardinterface = models.BigIntegerField()
    ip_address = models.BigIntegerField()
    isindicator2 = models.BigIntegerField()
    iskeyboard2 = models.BigIntegerField()
    indicator_firmware2 = models.BigIntegerField()
    indicator_hardware2 = models.BigIntegerField()
    keyboard_firmware2 = models.BigIntegerField()
    keyboard_hardware2 = models.BigIntegerField()
    keyboardinterface2 = models.BigIntegerField()
    interfacepanel2 = models.IntegerField()
    versionfamilyconfig = models.BigIntegerField()
    typemoduleindicator = models.BigIntegerField()
    typemodulekeyboard = models.BigIntegerField()
    isgps = models.BigIntegerField()
    isembedded_ethernet = models.BigIntegerField()
    isethdeviceoio1 = models.BigIntegerField()
    ethdeviceoio_firmware1 = models.BigIntegerField()
    ethdeviceoio_hardware1 = models.BigIntegerField()
    isethdeviceoio2 = models.BigIntegerField()
    ethdeviceoio_firmware2 = models.BigIntegerField()
    ethdeviceoio_hardware2 = models.BigIntegerField()
    typemoduleethdeviceio1 = models.BigIntegerField()
    typemoduleethdeviceio2 = models.BigIntegerField()
    subtypemoduleethdeviceio1 = models.BigIntegerField()
    subtypemoduleethdeviceio2 = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'controller_info'


class ControllerOrgs(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    id_org = models.ForeignKey(Organizations, models.DO_NOTHING, db_column='id_org')

    class Meta:
        managed = False
        db_table = 'controller_orgs'


class ControllerPrinter(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    type = models.BigIntegerField()
    header1 = models.TextField(blank=True, null=True)
    header2 = models.TextField(blank=True, null=True)
    footer = models.TextField(blank=True, null=True)
    param1 = models.BigIntegerField()
    param2 = models.BigIntegerField()
    param3 = models.BigIntegerField()
    param4 = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'controller_printer'


class ControllerReboot(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    date_time_on = models.DateTimeField()
    date_time_off = models.DateTimeField()
    reset_source = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'controller_reboot'


class ControllerUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    id_user = models.ForeignKey(Users, models.DO_NOTHING, db_column='id_user')
    needwrite = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'controller_users'


class DbVersion(models.Model):
    name = models.TextField()
    major = models.BigIntegerField()
    minor = models.BigIntegerField()
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'db_version'


class EventData(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    event_date_time = models.DateTimeField()
    event_type = models.BigIntegerField()
    event_in = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'event_data'


class FuelDispensingSynchronization(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_time = models.DateTimeField(blank=True, null=True)
    id_controller = models.BigIntegerField(blank=True, null=True)
    litre_lvl_meter = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    litre_journal = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    iduser = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fuel_dispensing_synchronization'


class Fuelprices(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_org = models.BigIntegerField()
    id_fueltype = models.ForeignKey(FuelsType, models.DO_NOTHING, db_column='id_fueltype')
    price = models.DecimalField(max_digits=15, decimal_places=2)
    deleted = models.BigIntegerField()
    date_add = models.DateTimeField()
    date_delete = models.DateTimeField(blank=True, null=True)
    date_change_config = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fuelprices'


class GsmModem(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    gprs_apn = models.TextField()
    gprs_user = models.TextField(blank=True, null=True)
    gprs_password = models.TextField(blank=True, null=True)
    server_name = models.TextField()
    server_port = models.BigIntegerField()
    server_ping = models.BigIntegerField()
    server_param1 = models.BigIntegerField()
    server_param2 = models.BigIntegerField()
    server_param3 = models.BigIntegerField()
    sms_pwd = models.TextField()
    networktypeselectionmode = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'gsm_modem'


class GsmModemLogger(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    id_message = models.IntegerField()
    date_time = models.DateTimeField()
    type_major = models.IntegerField()
    type_minor = models.IntegerField()
    error = models.IntegerField()
    cme_error = models.IntegerField()
    modem_error = models.IntegerField()
    state_error = models.IntegerField()
    count_error = models.IntegerField()
    param1 = models.IntegerField()
    param2 = models.IntegerField()
    param3 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'gsm_modem_logger'


class Journal(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    id_message = models.IntegerField()
    date_time = models.DateTimeField()
    major = models.IntegerField()
    minor = models.IntegerField()
    iduser = models.BigIntegerField()
    params_32_0 = models.BigIntegerField()
    params_32_1 = models.BigIntegerField()
    params_32_2 = models.BigIntegerField()
    params_16_0 = models.BigIntegerField()
    params_16_1 = models.BigIntegerField()
    params_16_2 = models.BigIntegerField()
    params_16_3 = models.BigIntegerField()
    params_16_4 = models.BigIntegerField()
    error = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'journal'


class JournalReadParams(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    date = models.DateTimeField()
    max_messages = models.BigIntegerField()
    index_last_message = models.BigIntegerField()
    roll = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'journal_read_params'


class JournalV2(models.Model):
    id = models.BigAutoField(primary_key=True)
    idmessage = models.BigIntegerField()
    idcontroller = models.BigIntegerField()
    codeerror = models.BigIntegerField()
    timeinsecond = models.BigIntegerField()
    array_data = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'journal_v2'


class LevelMetersData(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_level_meter = models.ForeignKey(LevelMeters, models.DO_NOTHING, db_column='id_level_meter')
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    id_user = models.BigIntegerField()
    date_time = models.DateTimeField()
    level = models.DecimalField(max_digits=10, decimal_places=2)
    level_valid = models.BooleanField()
    temperature = models.DecimalField(max_digits=10, decimal_places=2)
    temperature_valid = models.BooleanField()
    fill = models.DecimalField(max_digits=15, decimal_places=2)
    fill_valid = models.BooleanField()
    all_volume = models.DecimalField(max_digits=15, decimal_places=2)
    all_volume_valid = models.BooleanField()
    mass = models.DecimalField(max_digits=15, decimal_places=2)
    mass_valid = models.BooleanField()
    density = models.DecimalField(max_digits=10, decimal_places=3)
    density_valid = models.BooleanField()
    fuel_volume = models.DecimalField(max_digits=15, decimal_places=2)
    fuel_volume_valid = models.BooleanField()
    level_water = models.DecimalField(max_digits=10, decimal_places=2)
    level_water_valid = models.BooleanField()
    level_critical = models.BigIntegerField()
    level_critical_valid = models.BooleanField()
    data_from = models.IntegerField()
    raw_data = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'level_meters_data'
     


class LevelMetersParams(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_level_meter = models.ForeignKey(LevelMeters, models.DO_NOTHING, db_column='id_level_meter')
    delay_after_filling = models.BigIntegerField()
    auto_write = models.BigIntegerField()
    volume_down = models.BigIntegerField()
    level_down = models.BigIntegerField()
    destiny_change = models.BigIntegerField()
    temperature_change = models.BigIntegerField()
    wate_level_change = models.BigIntegerField()
    param1 = models.BigIntegerField()
    param2 = models.BigIntegerField()
    param3 = models.BigIntegerField()
    param4 = models.BigIntegerField()
    param5 = models.IntegerField()
    param6 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'level_meters_params'


class LevelMetersReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    id_user = models.ForeignKey(Users, models.DO_NOTHING, db_column='id_user')
    id_car = models.ForeignKey(Cars, models.DO_NOTHING, db_column='id_car', blank=True, null=True)
    id_fuel = models.ForeignKey(FuelsType, models.DO_NOTHING, db_column='id_fuel')
    date_time = models.DateTimeField()
    litre = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    sleeve = models.BigIntegerField()
    to_level_meter_data = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    later_level_meter_data = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    raz = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'level_meters_report'


class LinkType(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.BigIntegerField()
    name = models.TextField()
    comport_name = models.TextField(blank=True, null=True)
    comport_speed = models.BigIntegerField(blank=True, null=True)
    server_addr = models.TextField(blank=True, null=True)
    server_port = models.BigIntegerField(blank=True, null=True)
    server_user_name = models.TextField(blank=True, null=True)
    server_user_passwd = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_type'


class LmTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_lm = models.ForeignKey(LevelMeters, models.DO_NOTHING, db_column='id_lm')
    id_point = models.IntegerField()
    level_mm = models.IntegerField()
    volume = models.IntegerField()
    reserv = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'lm_table'


class LogActionUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_time_action = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    id_user = models.BigIntegerField(blank=True, null=True)
    ip_address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_action_users'


class LogConnects(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.BigIntegerField()
    date_time = models.DateTimeField()
    csq = models.BigIntegerField()
    err = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'log_connects'


class MonitoringSoftware(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip_address = models.TextField()
    name_computer = models.TextField()
    version_software = models.TextField()
    date_time_end_run = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'monitoring_software'


class Oildepots(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    deleted = models.BigIntegerField()
    date_delete = models.DateTimeField(blank=True, null=True)
    extern_code = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'oildepots'


class PlanFillings(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_org = models.ForeignKey(Organizations, models.DO_NOTHING, db_column='id_org', blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    litre = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    id_fuel_type = models.ForeignKey(FuelsType, models.DO_NOTHING, db_column='id_fuel_type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plan_fillings'


class PlanGroupFillings(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_group_tank = models.ForeignKey(GroupTanks, models.DO_NOTHING, db_column='id_group_tank', blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    litre = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    id_fuel_type = models.ForeignKey(FuelsType, models.DO_NOTHING, db_column='id_fuel_type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plan_group_fillings'


class PlanTankFillings(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_tank = models.ForeignKey(Tanks, models.DO_NOTHING, db_column='id_tank', blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    litre = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    id_fuel_type = models.ForeignKey(FuelsType, models.DO_NOTHING, db_column='id_fuel_type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plan_tank_fillings'


class Pourings(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_section = models.ForeignKey(Sections, models.DO_NOTHING, db_column='id_section')
    operation_type = models.IntegerField()
    date_time = models.DateTimeField()
    id_user = models.ForeignKey(Users, models.DO_NOTHING, db_column='id_user')
    operation_source = models.IntegerField()
    operation_location = models.IntegerField()
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    invoice_date_time = models.DateTimeField(blank=True, null=True)
    invoice_volume = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    invoice_density = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    invoice_temperature = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    invoice_mass = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    start_date_time = models.DateTimeField(blank=True, null=True)
    start_level = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_volume = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    start_density = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    start_temperature = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    end_date_time = models.DateTimeField(blank=True, null=True)
    end_level = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    end_volume = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    end_density = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    end_temperature = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tank_truck_info = models.TextField(blank=True, null=True)
    tank_truck_driver = models.TextField(blank=True, null=True)
    tank_truck_full_volume = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    tank_truck_volume = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    tank_truck_density = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    fact_litre = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    fact_kg = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fact_density = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    date_time_corection = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    invoice_volume_delta = models.DecimalField(max_digits=15, decimal_places=3)
    invoice_volume_real = models.DecimalField(max_digits=15, decimal_places=3)
    first_edit = models.IntegerField()
    metre_stick_start = models.DecimalField(max_digits=10, decimal_places=2)
    metre_stick_end = models.DecimalField(max_digits=10, decimal_places=2)
    metre_stick_delta_volume = models.DecimalField(max_digits=15, decimal_places=3)
    edit_invoice_mass = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pourings'


class Pourings2(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_section = models.ForeignKey(Sections, models.DO_NOTHING, db_column='id_section')
    operation_type = models.IntegerField()
    date_time = models.DateTimeField()
    id_user = models.ForeignKey(Users, models.DO_NOTHING, db_column='id_user')
    operation_source = models.IntegerField()
    operation_location = models.IntegerField()
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    invoice_date_time = models.DateTimeField(blank=True, null=True)
    invoice_volume = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    invoice_density = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    invoice_temperature = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    invoice_mass = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    start_date_time = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    start_level = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_volume = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    start_density = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    start_temperature = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    end_date_time = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    end_level = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    end_volume = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    end_density = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    end_temperature = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tank_truck_info = models.TextField(blank=True, null=True)
    tank_truck_driver = models.TextField(blank=True, null=True)
    tank_truck_full_volume = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    tank_truck_volume = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    tank_truck_density = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    fact_litre = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    fact_kg = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fact_density = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    date_time_corection = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    pouring_ready = models.IntegerField()
    date_first = models.DateTimeField()
    invoice_volume_delta = models.DecimalField(max_digits=15, decimal_places=3)
    invoice_volume_real = models.DecimalField(max_digits=15, decimal_places=3)
    first_edit = models.IntegerField()
    metre_stick_start = models.DecimalField(max_digits=10, decimal_places=2)
    metre_stick_end = models.DecimalField(max_digits=10, decimal_places=2)
    metre_stick_delta_volume = models.DecimalField(max_digits=15, decimal_places=3)
    edit_invoice_mass = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pourings2'


class Refineries(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    deleted = models.BigIntegerField()
    date_delete = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'refineries'


class ReportLimitUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_filling = models.ForeignKey(Fillings, models.DO_NOTHING, db_column='id_filling')
    ost_limit_day = models.DecimalField(max_digits=15, decimal_places=3)
    ost_limit_month = models.DecimalField(max_digits=15, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'report_limit_users'


class TrkErrors(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    ret_code = models.IntegerField()
    error_code = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'trk_errors'


class TrkMechanical(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    type = models.BigIntegerField()
    used = models.BigIntegerField()
    fuel_type = models.BigIntegerField()
    doze_min = models.BigIntegerField()
    doze_max = models.BigIntegerField()
    volume_before_stop = models.FloatField()
    volume_after_start = models.FloatField()
    doze_stop_after_pump_off = models.BigIntegerField()
    stop_if_error_flow_sensor = models.BigIntegerField()
    time_show_last_doze = models.BigIntegerField()
    pump_control_output = models.BigIntegerField()
    pump_type_control = models.BigIntegerField()
    pump_start_delay = models.BigIntegerField()
    valve_gate_type = models.BigIntegerField()
    valve_gate_output = models.BigIntegerField()
    valve_gate_control = models.BigIntegerField()
    valve_decrease_type = models.BigIntegerField()
    valve_decrease_output = models.BigIntegerField()
    valve_decrease_control = models.BigIntegerField()
    flow_sensor_type = models.BigIntegerField()
    flow_sensor_counter_type = models.BigIntegerField()
    flow_sensor_input1 = models.BigIntegerField()
    flow_sensor_input2 = models.BigIntegerField()
    flow_sensor_impulse_length = models.FloatField()
    flow_sensor_impulse_first_time = models.BigIntegerField()
    flow_sensor_impulse_next_time = models.BigIntegerField()
    button_type = models.BigIntegerField()
    button_input = models.BigIntegerField()
    button_duration = models.BigIntegerField()
    impulse_count = models.BigIntegerField()
    adjusting_factor = models.BigIntegerField()
    hatch_open_type = models.IntegerField()
    hatch_open_input = models.IntegerField()
    interfacepanel = models.IntegerField()
    svoyclubservicepointnumber = models.BigIntegerField(blank=True, null=True)
    svoyclubserver1 = models.TextField(blank=True, null=True)
    svoyclubport1 = models.BigIntegerField(blank=True, null=True)
    svoyclubserver2 = models.TextField(blank=True, null=True)
    svoyclubport2 = models.BigIntegerField(blank=True, null=True)
    svoyclubfueltype = models.ForeignKey(FuelsType, models.DO_NOTHING, db_column='svoyclubfueltype', blank=True, null=True)
    svoyclubcurrency = models.IntegerField(blank=True, null=True)
    svoyclubtimeoutconnection = models.IntegerField(blank=True, null=True)
    svoyclubtimeoutshowerror = models.IntegerField(blank=True, null=True)
    svoyclubsettingsinterfaceuser = models.BigIntegerField(blank=True, null=True)
    count_change_k = models.IntegerField()
    summator = models.BigIntegerField()
    external_type_in1 = models.BigIntegerField()
    external_type_in2 = models.BigIntegerField()
    external_type_in3 = models.BigIntegerField()
    external_type_in4 = models.BigIntegerField()
    count_dispenser = models.BigIntegerField()
    address_flowrate = models.BigIntegerField()
    summator_idrow = models.BigIntegerField()
    status_read_flowrate = models.BigIntegerField()
    countk_flowrate = models.BigIntegerField()
    summator_flowrate = models.BigIntegerField()
    adjustingfactor_flowrate = models.BigIntegerField()
    countimpulse1l_flowrate = models.BigIntegerField()
    onindandkey = models.IntegerField()
    rundispvalveafterauth = models.BigIntegerField()
    rundispvalvewhendispvalveremoved = models.BigIntegerField()
    countethexternal = models.BigIntegerField()
    supportmonitoringtransport = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'trk_mechanical'


class TrkSmart(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    type = models.BigIntegerField()
    subtype = models.BigIntegerField()
    address = models.BigIntegerField()
    reserve = models.BigIntegerField()
    speed = models.BigIntegerField()
    data_bits = models.BigIntegerField()
    stop_bits = models.BigIntegerField()
    parity = models.BigIntegerField()
    version = models.BigIntegerField()
    address2 = models.IntegerField()
    address3 = models.IntegerField()
    address4 = models.IntegerField()
    address5 = models.IntegerField()
    address6 = models.IntegerField()
    address7 = models.IntegerField()
    address8 = models.IntegerField()
    fuel_type2 = models.IntegerField()
    fuel_type3 = models.IntegerField()
    fuel_type4 = models.IntegerField()
    fuel_type5 = models.IntegerField()
    fuel_type6 = models.IntegerField()
    fuel_type7 = models.IntegerField()
    fuel_type8 = models.IntegerField()
    mode_filling = models.IntegerField()
    run_from_start_button = models.IntegerField(blank=True, null=True)
    mode_rfid = models.IntegerField()
    mode_topaz20 = models.IntegerField()
    count_party = models.BigIntegerField()
    count_typefuel = models.BigIntegerField()
    address1_party = models.BigIntegerField()
    address2_party = models.BigIntegerField()
    interface_trk = models.BigIntegerField()
    address_trk = models.BigIntegerField()
    index_dispenser = models.BigIntegerField()
    fuel_type1 = models.BigIntegerField()
    address9 = models.BigIntegerField()
    address10 = models.BigIntegerField()
    fuel_type9 = models.BigIntegerField()
    fuel_type10 = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'trk_smart'


class TrkSummator(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_controller = models.ForeignKey(Controllers, models.DO_NOTHING, db_column='id_controller')
    index_trk = models.IntegerField()
    summator = models.FloatField()
    date_read = models.DateTimeField()
    doze = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'trk_summator'