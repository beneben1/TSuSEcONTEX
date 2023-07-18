// apiContext.tsx
import React, { createContext, useState, ReactNode, useEffect } from "react";

interface Product {
    id: number;
    desc: string;
}

export interface APIContextType {
    products: Product[] | null;
    getProducts: () => Promise<void>;
}

export const APIContext = createContext<APIContextType | null>(null);

type APIProviderProps = {
    children: ReactNode;
};

export const APIProvider: React.FC<APIProviderProps> = ({ children }) => {
    const [apiState, setApiState] = useState<APIContextType>({
        products: null,
        getProducts: async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/products');
                const data = await response.json();
                setApiState((prevState) => ({
                    ...prevState,
                    products: data,
                }));
            } catch (error) {
                console.log(error);
            }
        },
    });

    useEffect(() => {
        apiState.getProducts();
    }, []);

    return (
        <APIContext.Provider value={apiState}>
            {children}
        </APIContext.Provider>
    );
};
