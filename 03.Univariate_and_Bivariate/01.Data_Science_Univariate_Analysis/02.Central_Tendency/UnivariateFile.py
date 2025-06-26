class UnivariateClass:
    # Creating a Function - quanQual (With Dataset as Parameter) To Automate to Separate Both Quantitive and Qualitative Columns with Return Statements of Created List(s) - quan, qual
    def quanQual(dataset):
        quan = []
        qual = []

        for columnName in dataset.columns:
            if dataset[columnName].dtype == 'O':
                qual.append(columnName)
                  
            elif dataset[columnName].dtype == 'bool':  # Boolean type
                qual.append(columnName)
            
            elif 'datetime' in str(dataset[columnName].dtype):  # Datetime types
                qual.append(columnName)
                
            elif dataset[columnName].dtype in ['int64', 'float64']:  # Numeric types
                quan.append(columnName)
            
            else:
                qual.append(columnName)
        
        return quan, qual

    # Creating a Function - OutlierColumnNames(with Parameter) To Automate by Finding out the Presence of Outliers in Column(s)
    def OutlierColumnNames(quan):
        LesserOutlierColumnName = []
        GreaterOutlierColumnName = []

        for checkOutlierColumnName in quan:
            if descriptive[checkOutlierColumnName]["MinValue"] < descriptive[checkOutlierColumnName]["LesserOutlier"]:
                LesserOutlierColumnName.append(checkOutlierColumnName)
            if descriptive[checkOutlierColumnName]["MaxValue"] > descriptive[checkOutlierColumnName]["GreaterOutlier"]:
                GreaterOutlierColumnName.append(checkOutlierColumnName)
        
        return f"{LesserOutlierColumnName}\n{GreaterOutlierColumnName}"

    # Creating a Function - ReplaceOutliers (with Parameter) To Automate by Replacing the Existing Outlier in Dataset
    def ReplaceOutliers(LesserOutlierColumnName, dataset, checkOutlierColumnName, GreaterOutlierColumnName):
        for columnName in LesserOutlierColumnName:
            dataset[columnName][dataset[columnName] < descriptive[checkOutlierColumnName]["LesserOutlier"]] = descriptive[checkOutlierColumnName]["LesserOutlier"]
        for columnName in GreaterOutlierColumnName:
            dataset[columnName][dataset[columnName] > descriptive[checkOutlierColumnName]["GreaterOutlier"]] = descriptive[checkOutlierColumnName]["GreaterOutlier"]

    # Creating a Function - Univariate (with Parameter) To Automate the Statistical Summary Table
    def Univariate(self, dataset, quan):
        descriptive = pd.DataFrame(
            index=["Mean", "Median", "Mode", "Q1:25%", "Q2:50%", "Q3:75%", "99%", "Q4:100%", "IQR", "1.5_rule",
                   "LesserOutlier", "GreaterOutlier", "MinValue", "MaxValue", "Skewness", "Kurtosis","Variance","StdDeviation"],
            columns=quan
        )

        for columnName in quan:
            descriptive[columnName]["Mean"] = dataset[columnName].mean()
            descriptive[columnName]["Median"] = dataset[columnName].median()
            descriptive[columnName]["Mode"] = dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"] = dataset.describe()[columnName]["25%"]
            descriptive[columnName]["Q2:50%"] = dataset.describe()[columnName]["50%"]
            descriptive[columnName]["Q3:75%"] = dataset.describe()[columnName]["75%"]
            descriptive[columnName]["99%"] = np.percentile(dataset[columnName], 99)
            descriptive[columnName]["Q4:100%"] = dataset.describe()[columnName]["max"]

            descriptive[columnName]["IQR"] = descriptive[columnName]["Q3:75%"] - descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5_rule"] = 1.5 * descriptive[columnName]["IQR"]
            descriptive[columnName]["LesserOutlier"] = descriptive[columnName]["Q1:25%"] - descriptive[columnName]["1.5_rule"]
            descriptive[columnName]["GreaterOutlier"] = descriptive[columnName]["Q3:75%"] + descriptive[columnName]["1.5_rule"]
            descriptive[columnName]["MinValue"] = dataset[columnName].min()
            descriptive[columnName]["MaxValue"] = dataset[columnName].max()
            
            descriptive[columnName]["Skewness"] = dataset[columnName].skew()
            descriptive[columnName]["Kurtosis"] = dataset[columnName].kurtosis()
            
            descriptive[columnName]["Variance"] = dataset[columnName].var()
            descriptive[columnName]["StdDeviation"] = dataset[columnName].std()

        return descriptive

    # Creating a Function - frequencyTable (with Parameter) To Automate the Frequency Table Generation
    def frequencyTable(dataset, columnName):
        frequencyTable = pd.DataFrame(columns=["Unique_Values", "Frequency", "Relative_Frequency", "CumSum"])
        frequencyTable["Unique_Values"] = dataset[columnName].value_counts().index
        frequencyTable["Frequency"] = dataset[columnName].value_counts().values
        frequencyTable["Relative_Frequency"] = frequencyTable["Frequency"] / 103
        frequencyTable["CumSum"] = frequencyTable["Relative_Frequency"].cumsum()
        
        return frequencyTable
