import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Upload } from 'lucide-react';

const HealthcareDashboard = () => {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    file: null
  });
  
  const [patientRecords, setPatientRecords] = useState([]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    setFormData(prevState => ({
      ...prevState,
      file: e.target.files[0]
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validate form data
    if (!formData.name || !formData.age || !formData.file) {
      alert('Please fill in all fields and upload a file');
      return;
    }

    // Add new record to the patient records
    const newRecord = {
      name: formData.name,
      age: formData.age,
      file: formData.file.name
    };
    
    setPatientRecords(prevRecords => [...prevRecords, newRecord]);

    // Clear form
    setFormData({
      name: '',
      age: '',
      file: null
    });

    alert('Data submitted successfully!');
  };

  return (
    <div className="container mx-auto p-6 max-w-full">
      <Card className="w-full mb-8">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center text-blue-600">
            Healthcare Patient Intake
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="name">Patient Name</Label>
              <Input 
                type="text" 
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Enter patient name"
                className="mt-2"
                required
              />
            </div>
            
            <div>
              <Label htmlFor="age">Patient Age</Label>
              <Input 
                type="number" 
                name="age"
                value={formData.age}
                onChange={handleInputChange}
                placeholder="Enter patient age"
                min="0"
                max="120"
                className="mt-2"
                required
              />
            </div>
            
            <div>
              <Label>Upload Medical Document</Label>
              <div className="flex items-center space-x-2 mt-2">
                <Input 
                  type="file" 
                  onChange={handleFileChange}
                  className="hidden"
                  id="file-upload"
                />
                <Label 
                  htmlFor="file-upload" 
                  className="flex items-center cursor-pointer 
                    border-2 border-dashed p-2 rounded-md 
                    hover:bg-blue-50 transition-colors"
                >
                  <Upload className="mr-2" />
                  {formData.file ? formData.file.name : 'Choose File'}
                </Label>
              </div>
            </div>
            <Button
              type="submit"
              className="w-full mt-4 bg-blue-600 hover:bg-blue-700"
            >
              Submit Patient Information
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Patient Records Table */}
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center text-blue-600">
            Patient Records
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="min-w-full table-auto border-collapse border border-gray-200">
              <thead>
                <tr className="bg-gray-100">
                  <th className="px-4 py-2 text-left border border-gray-300">Patient Name</th>
                  <th className="px-4 py-2 text-left border border-gray-300">Age</th>
                  <th className="px-4 py-2 text-left border border-gray-300">Uploaded File</th>
                </tr>
              </thead>
              <tbody>
                {patientRecords.length === 0 ? (
                  <tr>
                    <td colSpan="3" className="px-4 py-2 text-center text-gray-500 border border-gray-300">
                      No records available
                    </td>
                  </tr>
                ) : (
                  patientRecords.map((record, index) => (
                    <tr key={index} className="border-t">
                      <td className="px-4 py-2 border border-gray-300">{record.name}</td>
                      <td className="px-4 py-2 border border-gray-300">{record.age}</td>
                      <td className="px-4 py-2 border border-gray-300">{record.file}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default HealthcareDashboard;