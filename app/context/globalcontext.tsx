import React, { createContext, useContext, useState } from "react";
export const GlobalContext = createContext<{response: string, setResponse: React.Dispatch<React.SetStateAction<string>>} | undefined>(undefined);

export default function GlobalContextProvider({children}: {children: React.ReactNode}) {
    const [response, setResponse] = useState<string>("");

    return (
        <GlobalContext.Provider value={{response, setResponse}}>
            {children}
        </GlobalContext.Provider>
    )
}