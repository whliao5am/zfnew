def choose_class(self, browser):  # 选课
    # 快速选课
    browser.execute_script('window.open()')
    browser.switch_to_window(browser.window_handles[1])
    browser.get('http://jwc.xhu.edu.cn/xsxk.aspx?xh=3120170807112&xm=%C1%CE%CE%C4%BA%C0&gnmkdm=N121101')
    browser.find_element_by_xpath('/html/body/h2/a').click()
    browser.find_element_by_xpath('//*[@id="Button2"]').click()
    # 校公选课
    browser.find_element_by_xpath('//*[@id="Button2"]').click()
    browser.switch_to_window(browser.window_handles[2])
    browser.find_element_by_xpath('//*[@id="ListBox1"]/option').click()
    browser.find_element_by_xpath('//*[@id="Button1"]').click()
    browser.switch_to_window(browser.window_handles[1])

    n = len('//*[@id="kcmcgrid"]/tbody/tr[12]/td/b/*')
    index = False
    for i in range(2, n + 1):
        browser.find_element_by_xpath('//*[@id="kcmcgrid"]/tbody/tr[12]/td/b/a[' + str(i) + ']').click()
        for son in browser.find_elements_by_xpath('//*[@id="kcmcgrid"]/tbody/tr/td[1]/a'):
            if son.text == '151188019':
                son.click()
                index = True
                break

        while index:
            break
