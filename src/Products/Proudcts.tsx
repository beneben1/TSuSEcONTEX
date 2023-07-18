// Products.tsx
import React, { useContext } from 'react';
import { APIContext } from './apiContext';

const Products: React.FC = () => {
    const apiContext = useContext(APIContext);

    return (
        <div>
            {apiContext?.products ? (
                <table className="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {apiContext.products.map((product) => (
                            <tr key={product.id}>
                                <td>{product.id}</td>
                                <td>{product.desc}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>Loading Products....</p>
            )}
        </div>
    );
};

export default Products;
