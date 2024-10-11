
//rip 30 minutes of my life :sob:
public static boolean TestMethod(String methodName, Object result, Object... args) {
    try{
        Method[] methods = MethodHandles.lookup().lookupClass().getMethods();
        Method method = null;
        //find method, wont work with overloads
        for(Method m : methods) { 
            if(m.getName() == methodName){
                method = m;
                break;
            }
        }
        //muh static typed language
        Object testResult = method.invoke(null, args);
        try {
            if(result.getClass().getName().equals("java.lang.Double")) {
                //if this didnt fail then it probably is a double
                //round to 2 digits
                testResult = (double)Math.round(Double.parseDouble(testResult.toString()) * 100) / 100;
            }
            else if(result.getClass().getName().equals("java.lang.Integer")) {
                testResult = Integer.parseInt(testResult.toString());
            }
            //pass
            
        }
        catch(Exception e){ 
            //pass
        }
        boolean pass = testResult.toString().equals(result.toString());
        if(!pass) { 
            System.out.println("Failed unit test on: " + methodName);
            return pass;
        }
        System.out.println(methodName + " output: " + testResult.toString());

    } catch(Exception e){ 
        e.printStackTrace();
        return false;
    }
    
}